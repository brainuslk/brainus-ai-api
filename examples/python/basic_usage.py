"""
Basic Usage — BrainUs AI Python SDK

Requirements:
    pip install brainus-ai

Usage:
    export BRAINUS_API_KEY=your_api_key
    python basic_usage.py
"""

import asyncio
import os
from brainus_ai import BrainusAI, QueryFilters


async def main():
    api_key = os.getenv("BRAINUS_API_KEY")
    if not api_key:
        raise EnvironmentError("BRAINUS_API_KEY environment variable not set")

    async with BrainusAI(api_key=api_key) as client:

        # 1. Simple query — no filters
        print("1. Simple query")
        print("-" * 50)
        response = await client.query(query="What is Object-Oriented Programming?")
        print(f"Answer: {response.answer}\n")

        if response.has_citations:
            print("Citations:")
            for citation in response.citations:
                print(f"  - {citation.document_name} (Pages: {citation.pages})")
        print()

        # 2. Query with subject and grade filters
        print("2. Query with filters")
        print("-" * 50)
        response = await client.query(
            query="Explain the process of photosynthesis",
            filters=QueryFilters(subject="Biology", grade="10"),
        )
        print(f"Answer: {response.answer[:300]}...\n")

        # 3. Query with a specific model
        print("3. Query with brainusai-thinking model")
        print("-" * 50)
        response = await client.query(
            query="What are the differences between plant and animal cells?",
            model="brainusai-thinking",
            filters=QueryFilters(subject="Biology", grade="11"),
        )
        print(f"Answer: {response.answer[:300]}...\n")

        # 4. Usage statistics
        print("4. Usage statistics")
        print("-" * 50)
        stats = await client.get_usage()
        print(f"Total requests:  {stats.total_requests}")
        print(f"Quota used:      {stats.quota_percentage}%")
        if stats.quota_remaining:
            print(f"Quota remaining: {stats.quota_remaining}")
        print()

        # 5. Available plans
        print("5. Available plans")
        print("-" * 50)
        plans = await client.get_plans()
        for plan in plans:
            print(f"{plan.name}:")
            print(f"  Rate limit:    {plan.rate_limit_per_minute} req/min")
            print(f"  Monthly quota: {plan.monthly_quota or 'Unlimited'}")
            print(f"  Price:         LKR {plan.price_lkr or 0}/month")


if __name__ == "__main__":
    asyncio.run(main())
