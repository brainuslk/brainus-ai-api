#!/usr/bin/env bash
# BrainUs AI API — cURL Examples
#
# Usage:
#   export BRAINUS_API_KEY=your_api_key
#   bash basic.sh

set -e

BASE_URL="https://api.brainus.lk"
API_KEY="${BRAINUS_API_KEY:?BRAINUS_API_KEY is not set}"

echo "BrainUs AI API — cURL Examples"
echo "==============================="
echo ""

# 1. Simple query
echo "1. Simple query"
echo "---------------"
curl -s -X POST "$BASE_URL/api/v1/dev/query" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Object-Oriented Programming?"
  }' | jq '{ answer: .answer, citations: (.citations | length) }'
echo ""

# 2. Query with subject and grade filters
echo "2. Query with filters (Biology, Grade 10)"
echo "-----------------------------------------"
curl -s -X POST "$BASE_URL/api/v1/dev/query" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain the process of photosynthesis",
    "filters": {
      "subject": "Biology",
      "grade": "10"
    }
  }' | jq '{ answer: .answer[:200], citations: .citations }'
echo ""

# 3. Query with a specific model
echo "3. Query with brainusai-thinking model"
echo "---------------------------------------"
curl -s -X POST "$BASE_URL/api/v1/dev/query" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the differences between plant and animal cells?",
    "model": "brainusai-thinking",
    "filters": {
      "subject": "Biology",
      "grade": "11"
    }
  }' | jq '.answer[:200]'
echo ""

# 4. Check usage statistics
echo "4. Usage statistics"
echo "-------------------"
curl -s -X GET "$BASE_URL/api/v1/dev/usage" \
  -H "X-API-Key: $API_KEY" | jq '.'
echo ""

# 5. List available plans
echo "5. Available plans"
echo "------------------"
curl -s -X GET "$BASE_URL/api/v1/dev/plans" \
  -H "X-API-Key: $API_KEY" | jq '.[] | { name, rate_limit_per_minute, monthly_quota, price_lkr }'
