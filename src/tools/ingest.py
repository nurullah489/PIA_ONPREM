import os
import shutil
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# --- UPDATE THE BASE DIR PATH ---
BASE_DIR = r"..\PIA_ONPREM"
#----- 
DATA_PATH = os.path.join(BASE_DIR, "data", "raw_docs")
DB_PATH = os.path.join(BASE_DIR, "data", "vector_db")


def run_ingestion():
    print("--- Starting Priority-Aware Ingestion for Nomic v1.5 ---")
    
    # 1. CLEAN SLATE: Delete old DB to avoid dimension mismatch (384 vs 768)
    if os.path.exists(DB_PATH):
        print(f"Removing old database at {DB_PATH}...")
        shutil.rmtree(DB_PATH)

    all_chunks = []
    # Larger chunks (1000) are better for Nomic's 8k context window
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for filename in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, filename)
        
        try:
            if filename.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8") 
                docs = loader.load()
            elif filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                docs = loader.load()
            else:
                continue
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue

        # 2. Priority Logic
        is_web = any(x in filename.lower() for x in ["website", "_web", "content"])
        priority = 1 if is_web else 2
        source_type = "official_web" if priority == 1 else "internal_doc"
        
        chunks = text_splitter.split_documents(docs)
        for chunk in chunks:
            # 3. MANDATORY PREFIX for Nomic-Embed-Text v1.5
            # This is critical for retrieval quality
            chunk.page_content = f"search_document: {chunk.page_content}"
            
            chunk.metadata["priority"] = priority
            chunk.metadata["source_type"] = source_type
            chunk.metadata["file_name"] = filename
        
        all_chunks.extend(chunks)
        print(f"Processed: {filename} ({len(chunks)} chunks)")

    if not all_chunks:
        print("No documents found to ingest!")
        return

    # 4. Initialize Nomic (768-dim)
    # Ensure this matches the name in 'ollama list'
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # 5. Create Vector DB
    print(f"Embedding {len(all_chunks)} chunks... this may take a minute.")
    vectorstore = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    
    print(f"\nSUCCESS: Ingested {len(all_chunks)} chunks into Chroma (768-dim).")

if __name__ == "__main__":
    run_ingestion()