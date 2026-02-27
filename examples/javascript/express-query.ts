/**
 * Express.js API — BrainUs AI JavaScript/TypeScript SDK
 *
 * A simple Express server with a /query endpoint backed by BrainUs AI.
 *
 * Requirements:
 *   npm install @brainus/ai express
 *   npm install -D @types/express
 *
 * Usage:
 *   export BRAINUS_API_KEY=your_api_key
 *   npx tsx express-query.ts
 */

import express, { Request, Response } from "express";
import { BrainusAI, AuthenticationError, RateLimitError, QuotaExceededError } from "@brainus/ai";

const app = express();
app.use(express.json());

const client = new BrainusAI({ apiKey: process.env.BRAINUS_API_KEY! });

app.post("/query", async (req: Request, res: Response) => {
  const { query, subject, grade } = req.body;

  if (!query || typeof query !== "string") {
    return res.status(400).json({ error: "query is required" });
  }

  try {
    const response = await client.query({
      query,
      filters: subject && grade ? { subject, grade } : undefined,
    });

    res.json({
      answer: response.answer,
      citations: response.citations,
    });
  } catch (error) {
    if (error instanceof AuthenticationError) {
      return res.status(401).json({ error: "Invalid API key" });
    }
    if (error instanceof RateLimitError) {
      res.set("Retry-After", String(error.retryAfter ?? 60));
      return res.status(429).json({ error: "Rate limit exceeded" });
    }
    if (error instanceof QuotaExceededError) {
      return res.status(402).json({ error: "Monthly quota exceeded" });
    }
    console.error("BrainUs AI error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

const PORT = process.env.PORT ?? 3000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
  console.log(`POST http://localhost:${PORT}/query`);
});
