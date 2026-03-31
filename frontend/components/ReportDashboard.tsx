"use client";

import { ResearchResponse } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { CompetitorTable } from "./CompetitorTable";
import { GapCards } from "./GapCards";
import { LocationScoreCard } from "./LocationScoreCard";
import { TrafficCard } from "./TrafficCard";
import { MapPin, TrendingUp, Users, Lightbulb } from "lucide-react";

interface StatCardProps {
  label: string;
  value: string | number;
  sub?: string;
  icon: React.ReactNode;
}

function StatCard({ label, value, sub, icon }: StatCardProps) {
  return (
    <Card className="bg-card border-border">
      <CardContent className="pt-5">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">{label}</p>
            <p className="text-3xl font-bold">{value}</p>
            {sub && <p className="text-xs text-muted-foreground mt-0.5">{sub}</p>}
          </div>
          <div className="text-muted-foreground opacity-40">{icon}</div>
        </div>
      </CardContent>
    </Card>
  );
}

interface Props {
  report: ResearchResponse;
  onReset: () => void;
}

export function ReportDashboard({ report, onReset }: Props) {
  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold capitalize">{report.request_business_type} Market Analysis</h1>
          <p className="text-muted-foreground flex items-center gap-1.5 mt-1 text-sm">
            <MapPin className="w-3.5 h-3.5 shrink-0" />
            {report.request_address}
          </p>
        </div>
        <button
          onClick={onReset}
          className="text-xs text-muted-foreground hover:text-foreground transition-colors border border-border rounded px-3 py-1.5 shrink-0"
        >
          ← New search
        </button>
      </div>

      {/* Executive Summary */}
      <Card className="bg-card border-border border-l-4 border-l-emerald-500">
        <CardContent className="pt-5">
          <p className="text-xs text-emerald-400 uppercase tracking-wider font-semibold mb-2">
            Executive Summary
          </p>
          <p className="text-sm leading-relaxed">{report.executive_summary}</p>
        </CardContent>
      </Card>

      {/* Stat cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          label="Competitors"
          value={report.competitors.length}
          sub="in search radius"
          icon={<Users className="w-8 h-8" />}
        />
        <StatCard
          label="Location Score"
          value={`${Math.round(report.location_score.overall)}/100`}
          sub="suitability"
          icon={<MapPin className="w-8 h-8" />}
        />
        <StatCard
          label="Foot Traffic"
          value={report.traffic_estimate.estimated_daily_footfall}
          sub={`Peak: ${report.traffic_estimate.peak_day || "—"}`}
          icon={<TrendingUp className="w-8 h-8" />}
        />
        <StatCard
          label="Market Gaps"
          value={report.market_gaps.length}
          sub="opportunities found"
          icon={<Lightbulb className="w-8 h-8" />}
        />
      </div>

      {/* Location + Traffic */}
      <div className="grid md:grid-cols-2 gap-4">
        <LocationScoreCard score={report.location_score} />
        <TrafficCard traffic={report.traffic_estimate} />
      </div>

      {/* Competitors */}
      <section>
        <div className="flex items-center gap-3 mb-4">
          <h2 className="text-base font-semibold">Competitors</h2>
          <Separator className="flex-1" />
        </div>
        <CompetitorTable competitors={report.competitors} />
      </section>

      {/* Market Gaps */}
      <section>
        <div className="flex items-center gap-3 mb-4">
          <h2 className="text-base font-semibold">Market Gaps</h2>
          <Separator className="flex-1" />
        </div>
        <GapCards gaps={report.market_gaps} />
      </section>

      {/* Recommendations */}
      {report.recommendations.length > 0 && (
        <section>
          <div className="flex items-center gap-3 mb-4">
            <h2 className="text-base font-semibold">Recommendations</h2>
            <Separator className="flex-1" />
          </div>
          <div className="grid md:grid-cols-2 gap-3">
            {report.recommendations.map((rec, i) => (
              <div
                key={i}
                className="flex gap-3 p-4 rounded-lg border border-border bg-card"
              >
                <span className="text-emerald-500 font-bold text-sm shrink-0 mt-0.5">{i + 1}.</span>
                <p className="text-sm text-muted-foreground leading-relaxed">{rec}</p>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
