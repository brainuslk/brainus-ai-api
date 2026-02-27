/**
 * Basic Usage — BrainUs AI JavaScript/TypeScript SDK
 *
 * Requirements:
 *   npm install @brainus/ai
 *
 * Usage:
 *   export BRAINUS_API_KEY=your_api_key
 *   npx tsx basic-usage.ts
 */

import { BrainusAI, AuthenticationError, RateLimitError } from "@brainus/ai";

const apiKey = process.env.BRAINUS_API_KEY;
if (!apiKey) {
  console.error("BRAINUS_API_KEY environment variable not set");
  process.exit(1);
}

const client = new BrainusAI({ apiKey });

async function main() {
  try {
    // 1. Simple query — no filters
    console.log("1. Simple query");
    console.log("-".repeat(50));
    const response = await client.query({
      query: "What is Object-Oriented Programming?",
    });
    console.log(`Answer: ${response.answer}\n`);

    if (response.hasCitations) {
      console.log("Citations:");
      response.citations.forEach((c) => {
        console.log(`  - ${c.documentName} (Pages: ${c.pages.join(", ")})`);
      });
    }
    console.log();

    // 2. Query with subject and grade filters
    console.log("2. Query with filters");
    console.log("-".repeat(50));
    const filtered = await client.query({
      query: "Explain the process of photosynthesis",
      filters: { subject: "Biology", grade: "10" },
    });
    console.log(`Answer: ${filtered.answer.substring(0, 300)}...\n`);

    // 3. Query with a specific model
    console.log("3. Query with brainusai-thinking model");
    console.log("-".repeat(50));
    const thinking = await client.query({
      query: "What are the differences between plant and animal cells?",
      model: "brainusai-thinking",
      filters: { subject: "Biology", grade: "11" },
    });
    console.log(`Answer: ${thinking.answer.substring(0, 300)}...\n`);

    // 4. Usage statistics
    console.log("4. Usage statistics");
    console.log("-".repeat(50));
    const stats = await client.getUsage();
    console.log(`Total requests:  ${stats.totalRequests}`);
    console.log(`Quota used:      ${stats.quotaPercentage}%`);
    if (stats.quotaRemaining) {
      console.log(`Quota remaining: ${stats.quotaRemaining}`);
    }
    console.log();

    // 5. Available plans
    console.log("5. Available plans");
    console.log("-".repeat(50));
    const plans = await client.getPlans();
    plans.forEach((plan) => {
      console.log(`${plan.name}:`);
      console.log(`  Rate limit:    ${plan.rateLimitPerMinute} req/min`);
      console.log(`  Monthly quota: ${plan.monthlyQuota ?? "Unlimited"}`);
      console.log(`  Price:         LKR ${plan.priceLkr ?? 0}/month`);
    });
  } catch (error) {
    if (error instanceof AuthenticationError) {
      console.error("Authentication failed — check your API key");
    } else if (error instanceof RateLimitError) {
      console.error(`Rate limited. Retry after ${error.retryAfter}s`);
    } else {
      console.error("Error:", error);
    }
    process.exit(1);
  }
}

main();
