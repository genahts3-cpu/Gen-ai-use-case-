import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from app.config import settings
import os

# Initialize ChromaDB client
chroma_settings = Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_data",
    anonymized_telemetry=False
)

try:
    chroma_client = chromadb.HttpClient(
        host=settings.chroma_host,
        port=settings.chroma_port
    )
except Exception:
    # Fallback to local client
    chroma_client = chromadb.Client(chroma_settings)

# Initialize embeddings
embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)

def get_collection():
    """Get or create ChromaDB collection"""
    try:
        collection = chroma_client.get_collection(
            name=settings.chroma_collection_name
        )
    except Exception:
        collection = chroma_client.create_collection(
            name=settings.chroma_collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    return collection

def ingest_pdf(file_path: str, document_type: str = "policy"):
    """Ingest PDF documents into ChromaDB"""
    try:
        # Load PDF
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        # Split documents
        splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separator="\n"
        )
        chunks = splitter.split_documents(documents)
        
        # Get embeddings
        collection = get_collection()
        
        # Add to collection
        for i, chunk in enumerate(chunks):
            embedding = embeddings.embed_query(chunk.page_content)
            collection.add(
                ids=[f"{file_path}_{i}"],
                embeddings=[embedding],
                documents=[chunk.page_content],
                metadatas=[{
                    "source": file_path,
                    "document_type": document_type,
                    "page": chunk.metadata.get("page", 0)
                }]
            )
        
        return {"status": "success", "chunks": len(chunks)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_documents(query: str, top_k: int = 5):
    """Search documents in ChromaDB"""
    try:
        collection = get_collection()
        query_embedding = embeddings.embed_query(query)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return {
            "status": "success",
            "results": results,
            "query": query
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_rag_context(query: str, top_k: int = 3):
    """Get RAG context for a query"""
    search_results = search_documents(query, top_k)
    
    if search_results["status"] == "success":
        context = "\n".join([
            doc for doc in search_results["results"].get("documents", [[]])[0]
        ])
        return {
            "context": context,
            "sources": search_results["results"].get("metadatas", [[]])[0],
            "query": query
        }
    else:
        return {"context": "", "sources": [], "query": query, "error": search_results.get("message")}

def add_document_chunk(content: str, metadata: dict):
    """Add a document chunk to ChromaDB"""
    try:
        collection = get_collection()
        embedding = embeddings.embed_query(content)
        
        doc_id = metadata.get("id", f"doc_{len(collection.get()['ids'])}")
        
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[metadata]
        )
        
        return {"status": "success", "id": doc_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}
