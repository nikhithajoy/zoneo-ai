export interface ResearchRequest {
  address: string;
  business_type: string;
  radius_meters: number;
  max_competitors: number;
}

export interface Competitor {
  name: string;
  address: string;
  rating: number | null;
  user_ratings_total: number;
  price_level: number | null;
  distance_meters: number;
  competitive_score: number;
}

export interface LocationScore {
  overall: number;
  competition_density: number;
  accessibility_proxy: number;
  demand_signal: number;
  notes: string[];
}

export interface TrafficEstimate {
  busy_hours_summary: string;
  peak_day: string;
  estimated_daily_footfall: "low" | "medium" | "high";
  confidence: "low" | "medium" | "high";
  reasoning: string;
}

export interface MarketGap {
  gap_type: string;
  description: string;
  opportunity_score: number;
  supporting_evidence: string[];
}

export interface ResearchResponse {
  request_address: string;
  request_business_type: string;
  executive_summary: string;
  competitors: Competitor[];
  location_score: LocationScore;
  traffic_estimate: TrafficEstimate;
  market_gaps: MarketGap[];
  recommendations: string[];
}
