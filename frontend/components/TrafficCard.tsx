"use client";

import { TrafficEstimate } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const FOOTFALL_CONFIG = {
  high: { label: "High", color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" },
  medium: { label: "Medium", color: "bg-amber-500/20 text-amber-400 border-amber-500/30" },
  low: { label: "Low", color: "bg-muted text-muted-foreground border-border" },
};

const CONFIDENCE_CONFIG = {
  high: { label: "High confidence", color: "text-emerald-400" },
  medium: { label: "Medium confidence", color: "text-amber-400" },
  low: { label: "Low confidence", color: "text-muted-foreground" },
};

interface Props {
  traffic: TrafficEstimate;
}

export function TrafficCard({ traffic }: Props) {
  const footfallCfg = FOOTFALL_CONFIG[traffic.estimated_daily_footfall] ?? FOOTFALL_CONFIG.medium;
  const confidenceCfg = CONFIDENCE_CONFIG[traffic.confidence] ?? CONFIDENCE_CONFIG.medium;

  return (
    <Card className="bg-card border-border h-full">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
          Foot Traffic Estimate
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Footfall level */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Daily footfall</span>
          <Badge className={`${footfallCfg.color}`}>{footfallCfg.label}</Badge>
        </div>

        {/* Peak day */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Peak day</span>
          <span className="text-sm font-medium">{traffic.peak_day || "—"}</span>
        </div>

        {/* Busy hours */}
        <div>
          <p className="text-xs text-muted-foreground mb-1">Busy hours</p>
          <p className="text-sm">{traffic.busy_hours_summary || "—"}</p>
        </div>

        {/* Reasoning */}
        <div className="border-t border-border pt-3">
          <p className="text-xs text-muted-foreground mb-1">Analysis</p>
          <p className="text-xs text-muted-foreground leading-relaxed">{traffic.reasoning}</p>
          <p className={`text-xs mt-1 ${confidenceCfg.color}`}>{confidenceCfg.label}</p>
        </div>
      </CardContent>
    </Card>
  );
}
