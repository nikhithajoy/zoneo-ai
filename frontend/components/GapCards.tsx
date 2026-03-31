"use client";

import { MarketGap } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

function opportunityColor(score: number) {
  if (score >= 70) return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30";
  if (score >= 45) return "bg-amber-500/20 text-amber-400 border-amber-500/30";
  return "bg-muted text-muted-foreground";
}

interface Props {
  gaps: MarketGap[];
}

export function GapCards({ gaps }: Props) {
  if (gaps.length === 0) {
    return (
      <p className="text-muted-foreground text-sm py-4">
        No significant market gaps identified in this area.
      </p>
    );
  }

  const sorted = [...gaps].sort((a, b) => b.opportunity_score - a.opportunity_score);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {sorted.map((gap, i) => (
        <Card key={i} className="bg-card border-border">
          <CardHeader className="pb-2">
            <div className="flex items-start justify-between gap-2">
              <CardTitle className="text-sm font-semibold capitalize">
                {gap.gap_type.replace(/_/g, " ")}
              </CardTitle>
              <Badge className={`text-xs shrink-0 ${opportunityColor(gap.opportunity_score)}`}>
                {Math.round(gap.opportunity_score)}/100
              </Badge>
            </div>
            <Progress value={gap.opportunity_score} className="h-1 mt-1" />
          </CardHeader>
          <CardContent className="space-y-2">
            <p className="text-sm text-muted-foreground">{gap.description}</p>
            {gap.supporting_evidence.length > 0 && (
              <ul className="space-y-1">
                {gap.supporting_evidence.map((e, j) => (
                  <li key={j} className="text-xs text-muted-foreground flex gap-2">
                    <span className="text-emerald-500 mt-0.5 shrink-0">›</span>
                    {e}
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
