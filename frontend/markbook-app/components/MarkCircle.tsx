export function MarkCircle({
  value,
  size = 44,
}: {
  value: number;
  size?: number;
}) {
  return (
    <div
      className="relative inline-flex items-center justify-center shrink-0"
      style={{ width: size, height: size }}
    >
      <svg
        viewBox="0 0 100 100"
        className="absolute pointer-events-none"
        style={{
          top: -size * 0.2,
          left: -size * 0.2,
          width: size * 1.4,
          height: size * 1.4,
        }}
      >
        <path
          d="M50 6 C 76 6 92 24 90 50 C 88 76 70 92 46 90 C 20 88 8 68 10 46 C 12 22 30 6 50 6"
          fill="none"
          stroke="#B8412E"
          strokeWidth={3.5}
          strokeLinecap="round"
        />
      </svg>
      <span
        className="relative z-10 font-mono font-medium"
        style={{ color: "#B8412E", fontSize: size * 0.36 }}
      >
        {value}
      </span>
    </div>
  );
}
