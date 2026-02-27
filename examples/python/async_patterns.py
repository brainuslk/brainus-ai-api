"""
Async Patterns — BrainUs AI Python SDK

Demonstrates parallel queries and batch processing with asyncio.

Requirements:
    pip install brainus-ai

Usage:
    export BRAINUS_API_KEY=your_api_key
    python async_patterns.py
"""

import asyncio
import os
from brainus_ai import BrainusAI, QueryFilters


async def parallel_queries(queries: list[str]) -> list[dict]:
    """Run multiple queries at the same time instead of one by one."""
    async with BrainusAI(api_key=os.getenv("BRAINUS_API_KEY")) as client:
        tasks = [client.query(query=q) for q in queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    return [
        {
            "query": q,
            "answer": r.answer if not isinstance(r, Exception) else None,
            "error": str(r) if isinstance(r, Exception) else None,
        }
        for q, r in zip(queries, results)
    ]


async def batch_by_subject(subject: str, grade: str, queries: list[str]) -> list[dict]:
    """Query multiple questions for the same subject and grade in parallel."""
    async with BrainusAI(api_key=os.getenv("BRAINUS_API_KEY")) as client:
        tasks = [
            client.query(
                query=q,
                filters=QueryFilters(subject=subject, grade=grade),
            )
            for q in queries
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    return [
        {
            "query": q,
            "answer": r.answer[:150] + "..." if not isinstance(r, Exception) else None,
            "citations": len(r.citations) if not isinstance(r, Exception) else 0,
            "error": str(r) if isinstance(r, Exception) else None,
        }
        for q, r in zip(queries, results)
    ]


async def main():
    print("1. Parallel queries (no filters)")
    print("-" * 50)
    questions = [
        "What is Object-Oriented Programming?",
        "Explain the water cycle",
        "What is photosynthesis?",
    ]

    results = await parallel_queries(questions)
    for r in results:
        status = "OK" if not r["error"] else f"ERROR: {r['error']}"
        print(f"  [{status}] {r['query'][:50]}")
        if r["answer"]:
            print(f"    {r['answer'][:100]}...")
    print()

    print("2. Batch queries — Biology Grade 10")
    print("-" * 50)
    bio_questions = [
        "What is mitosis?",
        "Explain the difference between aerobic and anaerobic respiration",
        "What is the role of chlorophyll in photosynthesis?",
    ]

    results = await batch_by_subject("Biology", "10", bio_questions)
    for r in results:
        if r["answer"]:
            print(f"  Q: {r['query']}")
            print(f"  A: {r['answer']}")
            print(f"  Citations: {r['citations']}")
            print()


if __name__ == "__main__":
    asyncio.run(main())
