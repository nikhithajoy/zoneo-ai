"use client";

interface ScoreRingProps {
  score: number;
  size?: number;
  strokeWidth?: number;
  label?: string;
}

function scoreColor(score: number): string {
  if (score >= 70) return "#10b981"; // emerald
  if (score >= 45) return "#f59e0b"; // amber
  return "#ef4444"; // red
}

export function ScoreRing({ score, size = 120, strokeWidth = 10, label }: ScoreRingProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  const color = scoreColor(score);

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} className="-rotate-90">
        {/* Track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-muted"
          opacity={0.2}
        />
        {/* Progress */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{ transition: "stroke-dashoffset 0.6s ease" }}
        />
        {/* Score text (counter-rotate so it's upright) */}
        <text
          x="50%"
          y="50%"
          textAnchor="middle"
          dominantBaseline="central"
          className="rotate-90"
          style={{
            fill: color,
            fontSize: size * 0.22,
            fontWeight: 700,
            transform: `rotate(90deg)`,
            transformOrigin: "center",
          }}
        >
          {Math.round(score)}
        </text>
      </svg>
      {label && <p className="text-xs text-muted-foreground text-center">{label}</p>}
    </div>
  );
}
