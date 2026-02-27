"""
Error Handling — BrainUs AI Python SDK

Demonstrates how to handle authentication errors, rate limits,
quota exceeded, and other API errors.

Requirements:
    pip install brainus-ai

Usage:
    export BRAINUS_API_KEY=your_api_key
    python error_handling.py
"""

import asyncio
import os
from brainus_ai import (
    BrainusAI,
    BrainusError,
    AuthenticationError,
    RateLimitError,
    QuotaExceededError,
    APIError,
)


async def query_with_retry(query: str, max_retries: int = 3) -> dict | None:
    """Query with automatic retry on rate limit and transient API errors."""
    async with BrainusAI(api_key=os.getenv("BRAINUS_API_KEY")) as client:
        for attempt in range(max_retries):
            try:
                result = await client.query(query=query)
                return {"answer": result.answer, "attempts": attempt + 1}

            except AuthenticationError as e:
                # Wrong or missing API key — no point retrying
                print(f"Authentication failed: {e}")
                print("Check your BRAINUS_API_KEY.")
                return None

            except RateLimitError as e:
                # Too many requests — wait and retry
                wait = e.retry_after or 5
                print(f"Rate limited. Waiting {wait}s... (attempt {attempt + 1}/{max_retries})")
                await asyncio.sleep(wait)

            except QuotaExceededError:
                # Monthly quota hit — no point retrying
                print("Monthly quota exceeded. Upgrade your plan at developers.brainus.lk")
                return None

            except APIError as e:
                # Transient server error — retry with exponential backoff
                if attempt < max_retries - 1:
                    wait = 2 ** attempt
                    print(f"API error, retrying in {wait}s... ({e})")
                    await asyncio.sleep(wait)
                else:
                    print(f"API error after {max_retries} attempts: {e}")
                    return None

            except BrainusError as e:
                print(f"Unexpected error: {e}")
                return None

    return None


async def main():
    print("Error handling examples")
    print("=" * 50)

    # Successful query with retry logic
    result = await query_with_retry("What is photosynthesis?")
    if result:
        print(f"Success (attempts: {result['attempts']})")
        print(f"Answer: {result['answer'][:150]}...")
    print()

    # Demonstrate bad API key
    print("Testing with invalid API key:")
    try:
        async with BrainusAI(api_key="invalid_key") as client:
            await client.query(query="test")
    except AuthenticationError as e:
        print(f"Caught AuthenticationError: {e}")


if __name__ == "__main__":
    asyncio.run(main())
