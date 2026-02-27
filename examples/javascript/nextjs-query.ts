/**
 * Next.js Route Handler — BrainUs AI JavaScript/TypeScript SDK
 *
 * Example of a Next.js App Router API route that proxies queries
 * to BrainUs AI from the server side.
 *
 * File: app/api/query/route.ts
 *
 * Requirements:
 *   npm install @brainus/ai
 */

import { BrainusAI, AuthenticationError, RateLimitError, QuotaExceededError } from "@brainus/ai";
import { NextRequest, NextResponse } from "next/server";

const client = new BrainusAI({ apiKey: process.env.BRAINUS_API_KEY! });

export async function POST(request: NextRequest) {
  const body = await request.json();
  const { query, subject, grade } = body;

  if (!query || typeof query !== "string") {
    return NextResponse.json({ error: "query is required" }, { status: 400 });
  }

  try {
    const response = await client.query({
      query,
      filters: subject && grade ? { subject, grade } : undefined,
    });

    return NextResponse.json({
      answer: response.answer,
      citations: response.citations,
    });
  } catch (error) {
    if (error instanceof AuthenticationError) {
      return NextResponse.json({ error: "Invalid API key" }, { status: 401 });
    }
    if (error instanceof RateLimitError) {
      return NextResponse.json(
        { error: "Rate limit exceeded", retryAfter: error.retryAfter },
        { status: 429 }
      );
    }
    if (error instanceof QuotaExceededError) {
      return NextResponse.json({ error: "Monthly quota exceeded" }, { status: 402 });
    }
    console.error("BrainUs AI error:", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}
