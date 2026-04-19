"""
RAG System with Qdrant Vector Store
Enables semantic search and multi-document analysis for financial reports
"""

import os
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import anthropic
from sentence_transformers import SentenceTransformer

load_dotenv()


@dataclass
class DocumentChunk:
    """Represents a chunk of text from a document"""
    chunk_id: str
    text: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None


class FinancialRAGSystem:
    """
    RAG system for financial document analysis using Qdrant vector store

    Features:
    - Semantic search across multiple documents
    - Multi-document comparison and analysis
    - Historical trend analysis
    - Context-aware retrieval for Claude
    """

    def __init__(
        self,
        collection_name: str = "financial_reports",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        qdrant_path: str = "./qdrant_storage",
        use_cloud: bool = False,
        qdrant_url: Optional[str] = None,
        qdrant_api_key: Optional[str] = None
    ):
        """
        Initialize RAG system

        Args:
            collection_name: Name for Qdrant collection
            embedding_model: HuggingFace embedding model
            qdrant_path: Local storage path (if not using cloud)
            use_cloud: Whether to use Qdrant Cloud
            qdrant_url: Qdrant Cloud URL
            qdrant_api_key: Qdrant Cloud API key
        """
        self.collection_name = collection_name

        # Initialize embedding model
        print(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()

        # Initialize Qdrant client
        if use_cloud:
            if not qdrant_url or not qdrant_api_key:
                raise ValueError("Qdrant URL and API key required for cloud mode")
            self.qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            print(f"Connected to Qdrant Cloud: {qdrant_url}")
        else:
            self.qdrant_client = QdrantClient(path=qdrant_path)
            print(f"Using local Qdrant storage: {qdrant_path}")

        # Initialize Claude client
        self.anthropic_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

        # Create collection if it doesn't exist
        self._initialize_collection()

    def _initialize_collection(self):
        """Create Qdrant collection if it doesn't exist"""
        collections = self.qdrant_client.get_collections().collections
        collection_names = [c.name for c in collections]

        if self.collection_name not in collection_names:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dim,
                    distance=Distance.COSINE
                )
            )
            print(f"Created collection: {self.collection_name}")
        else:
            print(f"Using existing collection: {self.collection_name}")

    def chunk_document(
        self,
        text: str,
        metadata: Dict[str, Any],
        chunk_size: int = 1000,
        overlap: int = 200
    ) -> List[DocumentChunk]:
        """
        Split document into overlapping chunks

        Args:
            text: Full document text
            metadata: Document metadata (company, period, type, etc.)
            chunk_size: Target characters per chunk
            overlap: Overlap between chunks

        Returns:
            List of DocumentChunk objects
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk_text.rfind('.')
                last_newline = chunk_text.rfind('\n')
                break_point = max(last_period, last_newline)
                if break_point > chunk_size * 0.5:  # Only break if > 50% through
                    end = start + break_point + 1
                    chunk_text = text[start:end]

            chunk = DocumentChunk(
                chunk_id=str(uuid.uuid4()),
                text=chunk_text.strip(),
                metadata={
                    **metadata,
                    'chunk_index': len(chunks),
                    'start_char': start,
                    'end_char': end
                }
            )
            chunks.append(chunk)

            start = end - overlap

        print(f"Created {len(chunks)} chunks from document")
        return chunks

    def add_document(
        self,
        text: str,
        metadata: Dict[str, Any],
        chunk_size: int = 1000,
        overlap: int = 200
    ) -> int:
        """
        Add document to vector store

        Args:
            text: Full document text
            metadata: Document metadata
            chunk_size: Characters per chunk
            overlap: Overlap between chunks

        Returns:
            Number of chunks added
        """
        print(f"\nAdding document: {metadata.get('company', 'Unknown')} - {metadata.get('period', 'Unknown')}")

        # Chunk document
        chunks = self.chunk_document(text, metadata, chunk_size, overlap)

        # Generate embeddings
        print("Generating embeddings...")
        texts = [chunk.text for chunk in chunks]
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)

        # Create points for Qdrant
        points = []
        for chunk, embedding in zip(chunks, embeddings):
            point = PointStruct(
                id=chunk.chunk_id,
                vector=embedding.tolist(),
                payload={
                    'text': chunk.text,
                    **chunk.metadata
                }
            )
            points.append(point)

        # Upload to Qdrant
        print(f"Uploading {len(points)} chunks to Qdrant...")
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        print(f"✅ Successfully added {len(points)} chunks")
        return len(points)

    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Semantic search across all documents

        Args:
            query: Search query
            top_k: Number of results to return
            filters: Metadata filters (e.g., {'company': 'Infosys'})

        Returns:
            List of search results with text and metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0]

        # Build Qdrant filter
        qdrant_filter = None
        if filters:
            from qdrant_client.models import Filter, FieldCondition, MatchValue
            conditions = [
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in filters.items()
            ]
            qdrant_filter = Filter(must=conditions)

        # Search
        results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding.tolist(),
            limit=top_k,
            query_filter=qdrant_filter
        )

        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                'text': result.payload['text'],
                'score': result.score,
                'metadata': {k: v for k, v in result.payload.items() if k != 'text'}
            })

        return formatted_results

    def ask_with_rag(
        self,
        question: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        model: str = "claude-sonnet-4-20250514"
    ) -> Dict[str, Any]:
        """
        Answer question using RAG with Claude

        Args:
            question: User question
            top_k: Number of chunks to retrieve
            filters: Metadata filters
            model: Claude model to use

        Returns:
            Dict with answer and sources
        """
        print(f"\nProcessing question: {question}")

        # Retrieve relevant chunks
        print(f"Retrieving top {top_k} relevant chunks...")
        search_results = self.search(query=question, top_k=top_k, filters=filters)

        if not search_results:
            return {
                'answer': "No relevant information found in the vector store.",
                'sources': [],
                'tokens_used': 0
            }

        # Build context from retrieved chunks
        context_parts = []
        for i, result in enumerate(search_results, 1):
            metadata = result['metadata']
            context_parts.append(
                f"[Source {i}] {metadata.get('company', 'Unknown')} - "
                f"{metadata.get('period', 'Unknown')} - {metadata.get('document_type', 'Unknown')}\n"
                f"{result['text']}\n"
                f"(Relevance: {result['score']:.2f})\n"
            )

        context = "\n".join(context_parts)

        # Create prompt for Claude
        prompt = f"""You are analyzing financial documents. Use the retrieved context below to answer the question.

Retrieved Context:
{context}

Question: {question}

Instructions:
- Answer based on the retrieved context
- Cite sources by their [Source N] numbers
- If information is missing, clearly state what's not available
- Provide specific numbers and dates when available
- Be concise and accurate

Answer:"""

        # Call Claude
        print("Calling Claude for analysis...")
        response = self.anthropic_client.messages.create(
            model=model,
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        answer = response.content[0].text
        tokens_used = response.usage.input_tokens + response.usage.output_tokens

        return {
            'answer': answer,
            'sources': search_results,
            'tokens_used': tokens_used,
            'cost_estimate': (response.usage.input_tokens * 0.003 / 1000) +
                           (response.usage.output_tokens * 0.015 / 1000)
        }

    def compare_documents(
        self,
        question: str,
        doc_filters: List[Dict[str, Any]],
        model: str = "claude-sonnet-4-20250514"
    ) -> Dict[str, Any]:
        """
        Compare multiple documents (e.g., Q1 vs Q2 vs Q3)

        Args:
            question: Comparison question
            doc_filters: List of filters for each document
            model: Claude model

        Returns:
            Comparison analysis
        """
        print(f"\nComparing {len(doc_filters)} documents...")

        all_contexts = []
        for i, filters in enumerate(doc_filters, 1):
            results = self.search(query=question, top_k=3, filters=filters)
            if results:
                metadata = results[0]['metadata']
                doc_label = f"{metadata.get('company', 'Unknown')} - {metadata.get('period', 'Unknown')}"
                all_contexts.append(f"=== Document {i}: {doc_label} ===\n")
                for result in results:
                    all_contexts.append(result['text'] + "\n")

        context = "\n".join(all_contexts)

        prompt = f"""You are comparing financial documents across different time periods or entities.

Context from multiple documents:
{context}

Question: {question}

Instructions:
- Compare and contrast the information across documents
- Highlight key differences and trends
- Provide specific numbers and percentages
- Note any missing information
- Structure your comparison clearly

Comparison Analysis:"""

        response = self.anthropic_client.messages.create(
            model=model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            'analysis': response.content[0].text,
            'tokens_used': response.usage.input_tokens + response.usage.output_tokens
        }

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        collection_info = self.qdrant_client.get_collection(self.collection_name)
        return {
            'total_chunks': collection_info.points_count,
            'vector_dimension': collection_info.config.params.vectors.size,
            'collection_name': self.collection_name
        }

    def clear_collection(self):
        """Delete all data from collection"""
        self.qdrant_client.delete_collection(self.collection_name)
        self._initialize_collection()
        print(f"✅ Cleared collection: {self.collection_name}")
