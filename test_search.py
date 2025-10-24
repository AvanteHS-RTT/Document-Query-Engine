#!/usr/bin/env python3
"""
Test script for RAG search functionality.
Tests the vector similarity search endpoint.
"""

import requests
import json
from typing import Optional


class SearchTester:
    """Test client for the AI service search endpoint."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"

    def test_health(self) -> bool:
        """Test if the service is running."""
        try:
            response = requests.get(f"{self.api_url}/health")
            if response.status_code == 200:
                print("✓ Service is healthy")
                return True
            else:
                print(f"✗ Health check failed: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("✗ Cannot connect to service. Is it running?")
            return False

    def chat(
        self, query: str, top_k: int = 5, include_sources: bool = True
    ) -> Optional[dict]:
        """
        Perform a RAG query (search + LLM response).

        Args:
            query: Your question
            top_k: Number of documents to retrieve
            include_sources: Whether to include source documents

        Returns:
            RAG results or None if failed
        """
        try:
            print(f"\n💬 Chat Query: '{query}'")
            print(f"   Retrieving {top_k} documents for context")

            response = requests.get(
                f"{self.api_url}/chat",
                params={"q": query, "top_k": top_k, "include_sources": include_sources},
            )

            if response.status_code == 200:
                result = response.json()
                print(f"\n{'=' * 70}")
                print("🤖 AI Response:")
                print(f"{'=' * 70}")
                print(result["answer"])
                print(f"{'=' * 70}\n")

                if include_sources and "sources" in result:
                    print(f"📚 Source Documents ({len(result['sources'])}):\n")
                    for i, source in enumerate(result["sources"], 1):
                        print(
                            f"{i}. {source['file_name']} (score: {source['similarity_score']:.4f})"
                        )

                return result
            else:
                print(f"✗ Chat failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None

        except Exception as e:
            print(f"✗ Chat error: {str(e)}")
            return None

    def search(self, query: str, top_k: int = 5) -> Optional[dict]:
        """
        Perform a search query (search only, no LLM).

        Args:
            query: Search query text
            top_k: Number of results to return

        Returns:
            Search results or None if failed
        """
        try:
            print(f"\n🔍 Searching for: '{query}'")
            print(f"   Top K: {top_k}")

            response = requests.get(
                f"{self.api_url}/documents/search", params={"q": query, "top_k": top_k}
            )

            if response.status_code == 200:
                results = response.json()
                print(f"\n✓ Found {results['count']} results\n")

                # Display results
                for i, result in enumerate(results["results"], 1):
                    print(f"Result #{i}:")
                    print(f"  File: {result['file_name']}")
                    print(f"  Similarity Score: {result['similarity_score']:.4f}")
                    print(f"  Preview: {result['parsed_text_preview'][:150]}...")
                    print(f"  Created: {result['created_at']}")
                    print()

                return results
            else:
                print(f"✗ Search failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None

        except Exception as e:
            print(f"✗ Search error: {str(e)}")
            return None

    def list_documents(self) -> Optional[dict]:
        """List all uploaded documents."""
        try:
            print("\n📚 Listing all documents...")

            response = requests.get(f"{self.api_url}/documents")

            if response.status_code == 200:
                data = response.json()
                print(f"\n✓ Found {data['count']} documents\n")

                for i, doc in enumerate(data["documents"], 1):
                    print(f"{i}. {doc['file_name']}")
                    print(f"   ID: {doc['id']}")
                    print(f"   Embedding Size: {doc['embedding_size']}")
                    print(f"   Preview: {doc['parsed_text_preview'][:100]}...")
                    print()

                return data
            else:
                print(f"✗ List failed: {response.status_code}")
                return None

        except Exception as e:
            print(f"✗ List error: {str(e)}")
            return None


def main():
    """Run interactive search tests."""
    tester = SearchTester()

    print("=" * 70)
    print("RAG Search Test Tool")
    print("=" * 70)

    # Check service health
    if not tester.test_health():
        print("\n⚠ Service is not running. Please start it with:")
        print("  cd ai_service && python main.py")
        return

    while True:
        print("\n" + "=" * 70)
        print("Options:")
        print("  1. Chat (RAG: Search + LLM Response)")
        print("  2. Search documents only (no LLM)")
        print("  3. List all documents")
        print("  4. Run example queries")
        print("  5. Exit")
        print("=" * 70)

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            query = input("\nEnter your question: ").strip()
            if query:
                top_k = (
                    input("Number of context documents (default 5): ").strip() or "5"
                )
                sources = (
                    input("Include sources? (y/n, default y): ").strip().lower() or "y"
                )
                tester.chat(query, int(top_k), include_sources=(sources == "y"))

        elif choice == "2":
            query = input("\nEnter search query: ").strip()
            if query:
                top_k = input("Number of results (default 5): ").strip() or "5"
                tester.search(query, int(top_k))

        elif choice == "3":
            tester.list_documents()

        elif choice == "4":
            # Run some example queries
            example_queries = [
                "What is the node class?",
                "How does the search algorithm work?",
                "Explain the main architecture",
                "What are the key features?",
            ]

            print("\n🧪 Running example RAG queries...\n")
            for query in example_queries:
                tester.chat(query, top_k=3)
                input("\nPress Enter to continue to next query...")

        elif choice == "5":
            print("\n👋 Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
