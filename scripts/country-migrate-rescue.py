#!/usr/bin/env python3
"""Rescue pass for countries that failed shape_blog or shape_service in the
main mass migration run.

Root cause: the orchestrator deduplicated blog URLs against service URLs to
avoid scraping the same page twice. But many WP installs link to services
from the blog index (and vice versa) — so the dedupe wiped the actual
content of one kind, leaving an empty URL list and a downstream shape
failure.

This rescue:
  1. Re-discovers URLs for each failed (cc, kind) using a SMART dedupe that
     only removes a URL from the failed kind's list if it appears as a
     service-style URL pattern (contains /service/ or is in service list
     and the failed kind is blog).
  2. Re-runs the Playwright scrape for that kind only.
  3. Shapes, uploads heroes, and posts to Strapi.

Usage:
  python3 scripts/country-migrate-rescue.py [--dry-run]
"""

import os, sys, json, re, time, subprocess
from pathlib import Path

PROGRESS = Path("data/migration-progress.json")
LOG_DIR = Path("data/migration-logs")

DRY_RUN = "--dry-run" in sys.argv


def load_progress() -> dict:
    return json.loads(PROGRESS.read_text(encoding="utf-8")) if PROGRESS.exists() else {}


def save_progress(p: dict):
    PROGRESS.write_text(json.dumps(p, indent=2), encoding="utf-8")


def find_failed_kinds() -> list[tuple[str, str]]:
    """Return (cc, kind) tuples whose shape step failed."""
    out = []
    for cc, info in load_progress().items():
        for step, st in info.get("steps", {}).items():
            if step.startswith("shape_") and not st.get("ok"):
                kind = step.split("_", 1)[1]
                out.append((cc, kind))
    return sorted(set(out))


def smart_redisscover(cc: str) -> tuple[Path, Path]:
    """Re-run discovery using the authoritative Yoast sitemap classifier.
    No cross-dedupe — page-sitemap → services, post-sitemap → blogs."""
    log = LOG_DIR / cc / "rediscover.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    print(f"  [{cc}] rediscover...", end=" ", flush=True)
    if DRY_RUN:
        print("(dry)")
        return Path(f"data/{cc}/wp-blog-urls.txt"), Path(f"data/{cc}/wp-service-urls.txt")
    with open(log, "w", encoding="utf-8") as f:
        r = subprocess.run(["python3", "scripts/country-wp-discover.py", cc],
                           stdout=f, stderr=subprocess.STDOUT, timeout=600)
    print(f"rc={r.returncode}")
    return Path(f"data/{cc}/wp-blog-urls.txt"), Path(f"data/{cc}/wp-service-urls.txt")


def run_step(cc: str, label: str, cmd: list[str], log_path: Path,
             env: dict | None = None, timeout: int = 1800) -> bool:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"  [{cc}] {label:25s}...", end=" ", flush=True)
    t0 = time.time()
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    # Windows needs shell=True to resolve npx/node via PATH; matches orchestrator
    use_shell = sys.platform.startswith("win") and cmd and cmd[0] in ("npx", "node", "npm")
    cmd_str = " ".join(cmd) if use_shell else cmd
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            r = subprocess.run(cmd_str, stdout=f, stderr=subprocess.STDOUT,
                               env=full_env, timeout=timeout, shell=use_shell)
        ok = r.returncode == 0
        elapsed = time.time() - t0
        print(f"{'OK' if ok else 'FAIL'} ({elapsed:.0f}s)")
        return ok
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT after {timeout}s")
        return False


def rescue_kind(cc: str, kind: str, progress: dict):
    print(f"\n=== RESCUE {cc.upper()} / {kind} ===", flush=True)
    log_dir = LOG_DIR / cc
    state = progress.setdefault(cc, {"steps": {}})

    smart_redisscover(cc)

    url_file = Path(f"data/{cc}/wp-{kind}-urls.txt")
    if not url_file.exists() or not url_file.read_text(encoding="utf-8").strip():
        print(f"  [{cc}] {kind} URL list still empty after rescue discovery — skipping")
        state["steps"][f"shape_{kind}"] = {"ok": False, "err": "no urls (post-rescue)", "at": time.strftime('%Y-%m-%dT%H:%M:%SZ')}
        save_progress(progress)
        return

    if DRY_RUN:
        urls = url_file.read_text(encoding="utf-8").strip().splitlines()
        print(f"  [{cc}] {kind}: {len(urls)} URLs ready (dry-run)")
        return

    # Re-scrape with kind-specific env vars
    env = {"CC": cc, "KIND": kind}
    ok = run_step(cc, f"scrape_{kind}",
                  ["npx", "playwright", "test", "tests/country-wp-scrape.spec.ts", "--reporter=list"],
                  log_dir / f"rescue_scrape_{kind}.log", env=env, timeout=2400)
    state["steps"][f"scrape_{kind}"] = {"ok": ok, "err": "", "at": time.strftime('%Y-%m-%dT%H:%M:%SZ')}
    save_progress(progress)
    if not ok:
        return

    ok = run_step(cc, f"shape_{kind}",
                  ["python3", "scripts/country-shape-scraped.py", cc, kind],
                  log_dir / f"rescue_shape_{kind}.log", timeout=300)
    state["steps"][f"shape_{kind}"] = {"ok": ok, "err": "", "at": time.strftime('%Y-%m-%dT%H:%M:%SZ')}
    save_progress(progress)
    if not ok:
        return

    ok = run_step(cc, f"upload_{kind}_heroes",
                  ["python3", "-u", "scripts/country-upload-hero-images.py", cc, kind],
                  log_dir / f"rescue_upload_{kind}.log", timeout=900)
    state["steps"][f"upload_{kind}_heroes"] = {"ok": ok, "err": "", "at": time.strftime('%Y-%m-%dT%H:%M:%SZ')}
    save_progress(progress)
    if not ok:
        return

    ok = run_step(cc, f"post_{kind}",
                  ["python3", "-u", "scripts/country-post.py", cc, kind],
                  log_dir / f"rescue_post_{kind}.log", timeout=900)
    state["steps"][f"post_{kind}"] = {"ok": ok, "err": "", "at": time.strftime('%Y-%m-%dT%H:%M:%SZ')}
    save_progress(progress)


def rescue_post_only(cc: str, kind: str, progress: dict):
    """For countries where only the post step failed (Strapi timeout)."""
    print(f"\n=== RESCUE {cc.upper()} / post_{kind} ===", flush=True)
    log_dir = LOG_DIR / cc
    state = progress.setdefault(cc, {"steps": {}})
    if DRY_RUN:
        print(f"  (dry-run)")
        return
    ok = run_step(cc, f"post_{kind}",
                  ["python3", "-u", "scripts/country-post.py", cc, kind],
                  log_dir / f"rescue_post_{kind}.log", timeout=1200)
    state["steps"][f"post_{kind}"] = {"ok": ok, "err": "", "at": time.strftime('%Y-%m-%dT%H:%M:%SZ')}
    save_progress(progress)


def rescue_upload_only(cc: str, kind: str, progress: dict):
    """For countries where hero upload partially failed."""
    print(f"\n=== RESCUE {cc.upper()} / upload_{kind}_heroes ===", flush=True)
    log_dir = LOG_DIR / cc
    state = progress.setdefault(cc, {"steps": {}})
    if DRY_RUN:
        print("  (dry-run)")
        return
    ok = run_step(cc, f"upload_{kind}_heroes",
                  ["python3", "-u", "scripts/country-upload-hero-images.py", cc, kind],
                  log_dir / f"rescue_upload_{kind}.log", timeout=1800)
    state["steps"][f"upload_{kind}_heroes"] = {"ok": ok, "err": "", "at": time.strftime('%Y-%m-%dT%H:%M:%SZ')}
    save_progress(progress)
    if not ok:
        return
    # Chain post step after a successful upload
    ok = run_step(cc, f"post_{kind}",
                  ["python3", "-u", "scripts/country-post.py", cc, kind],
                  log_dir / f"rescue_post_{kind}.log", timeout=1200)
    state["steps"][f"post_{kind}"] = {"ok": ok, "err": "", "at": time.strftime('%Y-%m-%dT%H:%M:%SZ')}
    save_progress(progress)


def main():
    """Build a deduped action plan: shape failures supersede upload/post for
    the same (cc, kind) since rescue_kind chains everything downstream."""
    progress = load_progress()
    actions: dict[tuple[str, str], str] = {}  # (cc, kind) -> "shape"|"upload"|"post"
    for cc, info in progress.items():
        for step, st in info.get("steps", {}).items():
            if st.get("ok") or st.get("err") == "no urls":
                continue
            kind = None
            action = None
            if step in ("shape_blog", "shape_service"):
                kind = step.replace("shape_", "")
                action = "shape"
            elif step in ("post_blog", "post_service"):
                kind = step.replace("post_", "")
                action = "post"
            elif step in ("upload_blog_heroes", "upload_service_heroes"):
                kind = step.replace("upload_", "").replace("_heroes", "")
                action = "upload"
            if kind is None:
                continue
            key = (cc, kind)
            # shape > upload > post in priority (broader scope wins)
            current = actions.get(key)
            rank = {"shape": 3, "upload": 2, "post": 1}
            if current is None or rank[action] > rank[current]:
                actions[key] = action

    queue = sorted([(act, cc, kind) for (cc, kind), act in actions.items()])
    print(f"Rescue queue ({len(queue)}):", flush=True)
    for act, cc, kind in queue:
        print(f"  {act:6s} {cc} {kind}")

    t_start = time.time()
    for action, cc, kind in queue:
        try:
            if action == "shape":
                rescue_kind(cc, kind, progress)
            elif action == "post":
                rescue_post_only(cc, kind, progress)
            elif action == "upload":
                rescue_upload_only(cc, kind, progress)
        except Exception as e:
            print(f"  [{cc}] FATAL {e}", flush=True)
            progress.setdefault(cc, {})["fatal"] = str(e)
            save_progress(progress)

    print(f"\nRescue elapsed: {(time.time()-t_start)/60:.1f}m")


if __name__ == "__main__":
    main()
