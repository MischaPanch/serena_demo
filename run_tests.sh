#!/bin/bash

# Run all tests individually
echo "Running agent tests..."
python -m pytest tests/test_agent.py -v
echo ""

echo "Running parser tests..."
python -m pytest tests/test_parsers.py -v
echo ""

echo "Running notion adapter tests..."
python -m pytest tests/test_notion_adapter.py -v
echo ""

echo "Running LLM summarizer tests..."
python -m pytest tests/test_llm_summarizer.py -v
echo ""

echo "All tests complete!"
