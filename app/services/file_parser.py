"""
File parsing service for extracting text from various file formats.
Supports PDF, TXT, and other text-based formats.
"""

import io
from typing import Optional
from pypdf import PdfReader


class FileParser:
    """Service for parsing different file types and extracting text content."""

    @staticmethod
    async def parse_pdf(file_content: bytes) -> str:
        """
        Extract text from PDF file.

        Args:
            file_content: Raw PDF file bytes

        Returns:
            str: Extracted text content
        """
        try:
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)

            text_parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

            return "\n\n".join(text_parts)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")

    @staticmethod
    async def parse_txt(file_content: bytes) -> str:
        """
        Extract text from plain text file.

        Args:
            file_content: Raw text file bytes

        Returns:
            str: Extracted text content
        """
        try:
            # Try common encodings
            encodings = ["utf-8", "latin-1", "ascii", "utf-16"]

            for encoding in encodings:
                try:
                    return file_content.decode(encoding)
                except UnicodeDecodeError:
                    continue

            # If all encodings fail, use utf-8 with error replacement
            return file_content.decode("utf-8", errors="replace")
        except Exception as e:
            raise ValueError(f"Failed to parse text file: {str(e)}")

    @staticmethod
    async def parse_file(file_content: bytes, filename: str) -> str:
        """
        Parse a file based on its extension.

        Args:
            file_content: Raw file bytes
            filename: Original filename with extension

        Returns:
            str: Extracted text content

        Raises:
            ValueError: If file type is not supported
        """
        extension = filename.lower().split(".")[-1] if "." in filename else ""

        if extension == "pdf":
            return await FileParser.parse_pdf(file_content)
        elif extension in ["txt", "text", "md", "markdown"]:
            return await FileParser.parse_txt(file_content)
        else:
            raise ValueError(f"Unsupported file type: .{extension}")


# Global file parser instance
file_parser = FileParser()
