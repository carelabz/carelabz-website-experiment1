interface SAAnnouncementTickerProps {
  countryName: string;
  standards: string[];
}

export function SAAnnouncementTicker({
  countryName,
  standards,
}: SAAnnouncementTickerProps) {
  const primary = standards.slice(0, 3);
  const chunks =
    primary.length > 0
      ? primary
      : ["Global Power System Engineering", "50+ Countries"];

  return (
    <div className="bg-[#094d76] overflow-hidden py-3">
      <div className="animate-marquee whitespace-nowrap">
        {Array.from({ length: 4 }).map((_, i) => (
          <span key={i} className="inline-block mx-8">
            <span className="text-white text-sm font-medium tracking-wide">
              Carelabs
            </span>
            <span className="text-white/50 mx-4">—</span>
            <span className="text-white/70 text-sm">
              {countryName} Power System Engineering
            </span>
            {chunks.map((item, idx) => (
              <span key={idx} className="inline-block">
                <span className="text-[#F15C30] mx-4">•</span>
                <span className="text-white/70 text-sm">{item}</span>
              </span>
            ))}
            <span className="text-white/50 mx-4">—</span>
          </span>
        ))}
      </div>
    </div>
  );
}
