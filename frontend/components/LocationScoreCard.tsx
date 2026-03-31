"use client";

import { LocationScore } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScoreRing } from "./ScoreRing";
import { Progress } from "@/components/ui/progress";

const DIMENSIONS = [
  { key: "competition_density" as const, label: "Market Openness", invert: false },
  { key: "accessibility_proxy" as const, label: "Accessibility", invert: false },
  { key: "demand_signal" as const, label: "Demand Signal", invert: false },
];

interface Props {
  score: LocationScore;
}

export function LocationScoreCard({ score }: Props) {
  return (
    <Card className="bg-card border-border">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
          Location Score
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-5">
        <div className="flex justify-center">
          <ScoreRing score={score.overall} size={140} label="Overall suitability" />
        </div>

        <div className="space-y-3">
          {DIMENSIONS.map(({ key, label }) => (
            <div key={key}>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-muted-foreground">{label}</span>
                <span className="font-medium">{Math.round(score[key])}</span>
              </div>
              <Progress value={score[key]} className="h-1.5" />
            </div>
          ))}
        </div>

        {score.notes.length > 0 && (
          <ul className="space-y-1.5 border-t border-border pt-3">
            {score.notes.map((note, i) => (
              <li key={i} className="text-xs text-muted-foreground flex gap-2">
                <span className="text-emerald-500 shrink-0">›</span>
                {note}
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
