"""
Simple test script to verify the document upload functionality.
Run this after starting the server with: uv run uvicorn main:app --reload
"""

import httpx
import asyncio


async def test_upload():
    """Test the document upload endpoint."""

    # Create a simple test file
    test_content = """
    This is a test document for the AI service.

    It contains multiple paragraphs to test the embedding generation.
    The service should parse this text, generate an embedding,
    and store it in MongoDB.

    This is another paragraph to make the document longer
    and provide more content for the embedding model to process.
    """

    # Prepare the file for upload
    files = {"file": ("test_document.txt", test_content.encode("utf-8"), "text/plain")}

    # Upload the file
    async with httpx.AsyncClient() as client:
        print("📤 Uploading test document...")

        response = await client.post(
            "http://localhost:8000/api/v1/documents/upload", files=files
        )

        if response.status_code == 201:
            data = response.json()
            print("\n✅ Upload successful!")
            print(f"Document ID: {data['id']}")
            print(f"File Name: {data['file_name']}")
            print(f"Embedding Size: {data['embedding_size']}")
            print(f"Created At: {data['created_at']}")
            print(f"\nText Preview:")
            print(data["parsed_text_preview"])

            # Test retrieval
            doc_id = data["id"]
            print(f"\n📥 Retrieving document {doc_id}...")

            get_response = await client.get(
                f"http://localhost:8000/api/v1/documents/{doc_id}"
            )

            if get_response.status_code == 200:
                print("✅ Document retrieved successfully!")
            else:
                print(f"❌ Failed to retrieve document: {get_response.text}")

            # Test list
            print("\n📋 Listing documents...")
            list_response = await client.get(
                "http://localhost:8000/api/v1/documents?limit=10"
            )

            if list_response.status_code == 200:
                list_data = list_response.json()
                print(f"✅ Found {list_data['count']} documents")
            else:
                print(f"❌ Failed to list documents: {list_response.text}")

        else:
            print(f"\n❌ Upload failed: {response.status_code}")
            print(response.text)


if __name__ == "__main__":
    print("🧪 Testing AI Service Document Upload")
    print("=" * 50)
    asyncio.run(test_upload())
