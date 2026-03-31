"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { LoadingState } from "@/components/LoadingState";
import { ReportDashboard } from "@/components/ReportDashboard";
import { runResearch } from "@/lib/api";
import { ResearchResponse } from "@/lib/types";
import { Search, MapPin, Building2 } from "lucide-react";

const BUSINESS_TYPE_SUGGESTIONS = [
  "cafe", "restaurant", "gym", "pharmacy", "bakery",
  "bar", "supermarket", "clothing store", "bookstore", "yoga studio",
];

type State = "idle" | "loading" | "success" | "error";

export default function Home() {
  const [state, setState] = useState<State>("idle");
  const [address, setAddress] = useState("");
  const [businessType, setBusinessType] = useState("");
  const [radiusMeters, setRadiusMeters] = useState(1000);
  const [report, setReport] = useState<ResearchResponse | null>(null);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!address.trim() || !businessType.trim()) return;

    setState("loading");
    setError("");

    try {
      const result = await runResearch({
        address: address.trim(),
        business_type: businessType.trim(),
        radius_meters: radiusMeters,
        max_competitors: 20,
      });
      setReport(result);
      setState("success");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setState("error");
    }
  }

  function reset() {
    setState("idle");
    setReport(null);
    setError("");
  }

  if (state === "loading") {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <LoadingState address={address} businessType={businessType} />
      </div>
    );
  }

  if (state === "success" && report) {
    return <ReportDashboard report={report} onReset={reset} />;
  }

  // Idle / error — show search form
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-16">
      <div className="w-full max-w-lg space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
              <Search className="w-6 h-6 text-emerald-400" />
            </div>
          </div>
          <h1 className="text-3xl font-bold tracking-tight">Market Research Agent</h1>
          <p className="text-muted-foreground text-sm">
            AI-powered competitive analysis — competitors, location scores, foot traffic & market gaps.
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Address */}
          <div className="space-y-1.5">
            <Label htmlFor="address" className="text-sm font-medium flex items-center gap-1.5">
              <MapPin className="w-3.5 h-3.5" /> Target address
            </Label>
            <Input
              id="address"
              placeholder="e.g. Shoreditch High Street, London, UK"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              className="bg-card border-border"
              required
            />
          </div>

          {/* Business type */}
          <div className="space-y-1.5">
            <Label htmlFor="btype" className="text-sm font-medium flex items-center gap-1.5">
              <Building2 className="w-3.5 h-3.5" /> Business type
            </Label>
            <Input
              id="btype"
              placeholder="e.g. cafe, gym, restaurant"
              value={businessType}
              onChange={(e) => setBusinessType(e.target.value)}
              className="bg-card border-border"
              required
            />
            {/* Quick suggestions */}
            <div className="flex flex-wrap gap-1.5 pt-1">
              {BUSINESS_TYPE_SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setBusinessType(s)}
                  className={`text-xs px-2.5 py-1 rounded-full border transition-colors ${
                    businessType === s
                      ? "border-emerald-500 bg-emerald-500/10 text-emerald-400"
                      : "border-border text-muted-foreground hover:border-foreground/30"
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          {/* Radius */}
          <div className="space-y-1.5">
            <Label className="text-sm font-medium">
              Search radius —{" "}
              <span className="text-muted-foreground font-normal">
                {radiusMeters >= 1000 ? `${radiusMeters / 1000}km` : `${radiusMeters}m`}
              </span>
            </Label>
            <div className="flex items-center gap-3">
              <span className="text-xs text-muted-foreground w-10">250m</span>
              <input
                type="range"
                min={250}
                max={2000}
                step={250}
                value={radiusMeters}
                onChange={(e) => setRadiusMeters(Number(e.target.value))}
                className="flex-1 accent-emerald-500"
              />
              <span className="text-xs text-muted-foreground w-10 text-right">2km</span>
            </div>
          </div>

          {/* Error */}
          {state === "error" && (
            <p className="text-sm text-destructive bg-destructive/10 border border-destructive/20 rounded-lg px-4 py-3">
              {error}
            </p>
          )}

          <Button
            type="submit"
            className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium h-11"
            disabled={!address.trim() || !businessType.trim()}
          >
            Analyze Market
          </Button>
        </form>

        <p className="text-center text-xs text-muted-foreground">
          Powered by Claude + Google Places · takes ~2 min to run
        </p>
      </div>
    </div>
  );
}
