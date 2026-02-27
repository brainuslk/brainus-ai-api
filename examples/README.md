# Examples

Runnable code examples for the BrainUs AI API.

## Setup

All examples require a BrainUs AI API key. Get one at [developers.brainus.lk](https://developers.brainus.lk).

```bash
export BRAINUS_API_KEY=your_api_key
```

---

## Python

Requires Python 3.9+ and the `brainus-ai` package.

```bash
pip install brainus-ai
```

| File | Description |
|---|---|
| [basic_usage.py](./python/basic_usage.py) | Simple query, filters, usage stats, and plans |
| [async_patterns.py](./python/async_patterns.py) | Parallel queries and batch processing with asyncio |
| [error_handling.py](./python/error_handling.py) | Handling auth errors, rate limits, and quota errors |

**Run an example:**

```bash
python examples/python/basic_usage.py
```

---

## JavaScript / TypeScript

Requires Node.js 18+ and the `@brainus/ai` package.

```bash
npm install @brainus/ai
```

| File | Description |
|---|---|
| [basic-usage.ts](./javascript/basic-usage.ts) | Simple query with filters and citations |
| [nextjs-query.ts](./javascript/nextjs-query.ts) | Server-side queries in a Next.js route handler |
| [express-query.ts](./javascript/express-query.ts) | Express.js endpoint wrapping the BrainUs AI API |

**Run an example:**

```bash
npx tsx examples/javascript/basic-usage.ts
```

---

## cURL

No dependencies required.

| File | Description |
|---|---|
| [basic.sh](./curl/basic.sh) | Common API calls as shell scripts |

**Run an example:**

```bash
bash examples/curl/basic.sh
```
