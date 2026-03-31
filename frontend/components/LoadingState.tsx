"use client";

import { useEffect, useState } from "react";

const STEPS = [
  { label: "Geocoding address", duration: 4 },
  { label: "Finding nearby competitors", duration: 20 },
  { label: "Scoring location suitability", duration: 20 },
  { label: "Estimating foot traffic", duration: 20 },
  { label: "Identifying market gaps", duration: 20 },
  { label: "Synthesizing report", duration: 30 },
];

export function LoadingState({ address, businessType }: { address: string; businessType: string }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => setElapsed((e) => e + 1), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    let acc = 0;
    for (let i = 0; i < STEPS.length; i++) {
      acc += STEPS[i].duration;
      if (elapsed < acc) {
        setCurrentStep(i);
        break;
      }
      if (i === STEPS.length - 1) setCurrentStep(STEPS.length - 1);
    }
  }, [elapsed]);

  return (
    <div className="flex flex-col items-center gap-8 py-16 max-w-md mx-auto text-center">
      {/* Spinner */}
      <div className="relative w-20 h-20">
        <div className="absolute inset-0 rounded-full border-4 border-muted opacity-30" />
        <div className="absolute inset-0 rounded-full border-4 border-t-emerald-500 animate-spin" />
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-1">Analyzing the market…</h2>
        <p className="text-sm text-muted-foreground">
          <span className="font-medium text-foreground">{businessType}</span> near{" "}
          <span className="font-medium text-foreground">{address}</span>
        </p>
        <p className="text-xs text-muted-foreground mt-1">
          This takes 2–3 minutes · {elapsed}s elapsed
        </p>
      </div>

      {/* Steps */}
      <div className="w-full space-y-3 text-left">
        {STEPS.map((step, i) => {
          const done = i < currentStep;
          const active = i === currentStep;
          return (
            <div key={i} className="flex items-center gap-3">
              <div
                className={`w-5 h-5 rounded-full flex items-center justify-center text-xs flex-shrink-0 transition-colors ${
                  done
                    ? "bg-emerald-500 text-white"
                    : active
                    ? "bg-emerald-500/20 border border-emerald-500 text-emerald-400"
                    : "bg-muted/30 text-muted-foreground"
                }`}
              >
                {done ? "✓" : i + 1}
              </div>
              <span
                className={`text-sm transition-colors ${
                  done ? "text-muted-foreground line-through" : active ? "text-foreground" : "text-muted-foreground/50"
                }`}
              >
                {step.label}
                {active && <span className="animate-pulse">…</span>}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
