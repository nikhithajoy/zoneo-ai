"use client";

import { Competitor } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const PRICE_LABELS: Record<number, string> = { 0: "Free", 1: "$", 2: "$$", 3: "$$$", 4: "$$$$" };

function StarRating({ rating }: { rating: number | null }) {
  if (rating == null) return <span className="text-muted-foreground text-xs">—</span>;
  return (
    <span className="flex items-center gap-1">
      <span className="text-amber-400">★</span>
      <span className="text-sm font-medium">{rating.toFixed(1)}</span>
    </span>
  );
}

function ThreatBadge({ score }: { score: number }) {
  if (score >= 70) return <Badge variant="destructive">High</Badge>;
  if (score >= 45) return <Badge className="bg-amber-500/20 text-amber-400 border-amber-500/30">Medium</Badge>;
  return <Badge variant="outline" className="text-muted-foreground">Low</Badge>;
}

interface Props {
  competitors: Competitor[];
}

export function CompetitorTable({ competitors }: Props) {
  if (competitors.length === 0) {
    return (
      <p className="text-muted-foreground text-sm py-4">
        No competitors found in this radius.
      </p>
    );
  }

  const sorted = [...competitors].sort((a, b) => b.competitive_score - a.competitive_score);

  return (
    <div className="overflow-auto rounded-lg border border-border">
      <Table>
        <TableHeader>
          <TableRow className="hover:bg-transparent">
            <TableHead>Business</TableHead>
            <TableHead>Rating</TableHead>
            <TableHead>Reviews</TableHead>
            <TableHead>Price</TableHead>
            <TableHead>Distance</TableHead>
            <TableHead>Threat</TableHead>
            <TableHead className="w-32">Score</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {sorted.map((c, i) => (
            <TableRow key={i}>
              <TableCell>
                <div>
                  <p className="font-medium text-sm">{c.name}</p>
                  <p className="text-xs text-muted-foreground truncate max-w-[200px]">{c.address}</p>
                </div>
              </TableCell>
              <TableCell>
                <StarRating rating={c.rating} />
              </TableCell>
              <TableCell>
                <span className="text-sm">{c.user_ratings_total.toLocaleString()}</span>
              </TableCell>
              <TableCell>
                <span className="text-sm text-muted-foreground">
                  {c.price_level != null ? PRICE_LABELS[c.price_level] ?? "—" : "—"}
                </span>
              </TableCell>
              <TableCell>
                <span className="text-sm">{Math.round(c.distance_meters)}m</span>
              </TableCell>
              <TableCell>
                <ThreatBadge score={c.competitive_score} />
              </TableCell>
              <TableCell>
                <div className="flex items-center gap-2">
                  <Progress value={c.competitive_score} className="h-1.5 w-20" />
                  <span className="text-xs text-muted-foreground w-8">
                    {Math.round(c.competitive_score)}
                  </span>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
