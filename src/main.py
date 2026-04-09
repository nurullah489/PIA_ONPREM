
import os
import urllib3
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# --- 1. Environment ---

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 2. Path Configuration ---
# -----UPDATE BASE DIR 
BASE_DIR = r"...\PIA_ONPREM"
DB_PATH = os.path.join(BASE_DIR, "data", "vector_db")

def initialize_pia():
    print("--- Initializing PIA (Pubali Bank Assistant) ---")

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )

    if not os.path.exists(DB_PATH):
        print(f"Error: Vector DB not found at {DB_PATH}.")
        return None

    vectorstore = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    # Note: Using your 'pia-brain' which points to your llama-3.2 GGUF
    llm = ChatOllama(
        model="pia-brain",
        base_url="http://localhost:11434",
        temperature=0.1
    )

    # Updated Prompt with chat_history placeholder
    system_prompt = (
        "You are PIA (Personal Intelligent Assistant), the official AI for personal conversation.\n\n"
        "CORE RULES:\n"
        "1. LANGUAGE: Follow the user's language preference. If they ask for English, translate context if needed.\n"
        "2. ACCURACY: Use ONLY the provided context. If it's not there, say you don't have that info.\n\n"
        "Retrieved Context:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    
    return create_retrieval_chain(
        vectorstore.as_retriever(search_kwargs={"k": 5}), 
        combine_docs_chain
    )

def chat():
    pia = initialize_pia()
    if not pia: return

    # This list stores the conversation state
    chat_history = [] 

    print("\nPIA is online. Language: English/Bangla supported.")
    print("-" * 40)

    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("PIA: Thank you for your time. Goodbye!")
            break

        if not user_input.strip(): continue

        try:
            # Passing both input AND history to satisfy the PromptTemplate
            response = pia.invoke({
                "input": user_input, 
                "chat_history": chat_history
            })
            
            answer = response['answer']
            print(f"\nPIA: {answer}")

            # Update memory
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=answer))

            # Keep history to last 5 rounds (10 messages) to prevent slow response
            if len(chat_history) > 10:
                chat_history = chat_history[-10:]

        except Exception as e:
            print(f"\n[System Error]: {e}")

if __name__ == "__main__":
    chat()