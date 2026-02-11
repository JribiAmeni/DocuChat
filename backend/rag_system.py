import os
from dotenv import load_dotenv
from groq import Groq

from processing.text_extraction import load_documents
from processing.text_segmentation import segment_all_documents
from processing.embedding_generation import EmbeddingModel
from processing.vector_index import VectorIndex

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY missing")


class RAGSystem:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.embedder = EmbeddingModel()
        self.index = VectorIndex()
        self.documents = []
        self.all_chunks = []

    def reset(self):
        """Reset the RAG system completely - clears all indexed data"""
        self.index = VectorIndex()
        self.documents = []
        self.all_chunks = []
        print("🔄 RAG system reset complete")

    def load_docs(self, folder):
        """Load and index documents - automatically resets if documents already loaded"""
        try:
            # 🔄 Reset before loading new documents to ensure clean state
            if self.documents or self.all_chunks:
                print("🔄 Resetting RAG system before loading new documents...")
                self.reset()
            
            docs = load_documents(folder)
            if not docs:
                print("⚠️ No documents found in folder")
                return False
            
            # Store original documents
            self.documents = docs
            
            # Segment documents
            chunks = segment_all_documents(docs)
            self.all_chunks = chunks
            
            # Build index
            self.index.build(chunks, self.embedder)
            
            print(f"✅ Loaded {len(docs)} documents with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"❌ Error loading documents: {str(e)}")
            return False

    
    def ask(self, question):
        """Answer a question using RAG"""
        try:
            # Check if documents are indexed
            if not self.all_chunks:
                return "❌ No documents indexed. Please upload documents first."
            
            # Detect multi-document query
            is_multi_doc = self.is_multi_document_query(question)
            
            if is_multi_doc:
                print(f"\n🔗 Multi-document query detected")
                # Get more chunks for comprehensive answer
                top_k = min(15, len(self.all_chunks))
                results = self.index.search(question, self.embedder, top_k)
            else:
                # Regular query
                top_k = min(5, len(self.all_chunks))
                results = self.index.search(question, self.embedder, top_k)
            
            if not results:
                return "❌ No relevant information found in the documents."
            
    
            if not doc_contexts:
                return "❌ No relevant content found."
            
            # Build structured context
            context_parts = []
            for filename, texts in doc_contexts.items():
                combined = " ".join(texts)
                context_parts.append(f"=== Document: {filename} ===\n{combined}\n")
            
            context = "\n".join(context_parts)
            
            # Debug output
            print(f"\n📚 Using {len(doc_contexts)} document(s)")
            print(f"📊 Total chunks: {sum(len(texts) for texts in doc_contexts.values())}")
            
            # Create appropriate prompt
            if is_multi_doc:
                system_prompt = """You are a document analysis assistant. 
When analyzing multiple documents:
- Synthesize information from ALL documents provided
- Mention specific documents when citing information
- Provide a comprehensive overview
- Use clear formatting with bullet points and sections
- Be thorough but concise"""

                prompt = f"""Based on the following documents, please answer the question.

Documents:
{context}

Question: {question}

Provide a well-structured answer with:
• Clear sections or bullet points
• References to specific documents when relevant
• A comprehensive synthesis of all information

Answer:"""
            else:
                system_prompt = """You are a precise document assistant.
Answer questions based ONLY on the provided context.
If information is not in the context, say so clearly.
Use clear formatting with bullet points when appropriate."""

                prompt = f"""Context from documents:
{context}

Question: {question}

Answer based on the context above. If the answer is not in the context, say "I cannot find this information in the provided documents."

Answer:"""
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1500
            )
            
            answer = response.choices[0].message.content
            
            # Format answer for better readability
            formatted_answer = self.format_answer(answer, list(doc_contexts.keys()))
            
            return formatted_answer
            
        except Exception as e:
            error_msg = f"❌ Error generating answer: {str(e)}"
            print(error_msg)
            return error_msg

    def format_answer(self, answer, source_docs):
        """Format answer for better display"""
        # Add source information at the end
        sources = "\n\n---\n📚 Sources: " + ", ".join(source_docs)
        return answer + sources


def main():
    """CLI interface for testing"""
    rag = RAGSystem()
    folder = input("📂 Documents folder path: ").strip()

    if not rag.load_docs(folder):
        print("❌ Failed to load documents")
        return

    while True:
        q = input("\n❓ Question (or 'exit' to quit): ").strip()
        if q.lower() in ("exit", "quit", "q"):
            print("👋 Goodbye!")
            break
        
        if not q:
            continue
            
        print("\n🤔 Thinking...\n")
        answer = rag.ask(q)
        print("🤖 Answer:\n")
        print(answer)
        print("\n" + "="*60)


if __name__ == "__main__":
    main()