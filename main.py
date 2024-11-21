import os
import pickle
import time
from datetime import datetime
# from fastapi import query
from llama_index.core.chat_engine.types import StreamingAgentChatResponse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_parse import LlamaParse
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent

from fun_tools import get_tools
# from llama_index.llms import OpenAI
from prompts import context
# Function to save and load data using pickle
def save_data(obj, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)
def load_data(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

# Initialize the LLM with a timeout
llm = Ollama(model="llama3.2:1b", request_timeout=60.0)
# llm = OpenAI(model="gpt-4", api_key=os.getenv(""))


# Paths for serialized data
documents_file = 'serialize/documents.pkl'
vector_index_file = 'serialize/vector_index.pkl'

# Load or parse documents
if os.path.exists(documents_file):
    print("Loading pre-parsed documents...")
    documents = load_data(documents_file)
else:
    print("Parsing documents from PDF files...")
    parser = LlamaParse(api_key='', result_type='markdown')
    file_extractor = {'.pdf': parser}
    documents = SimpleDirectoryReader('data/', file_extractor=file_extractor).load_data()
    save_data(documents, documents_file)

# Load or build the vector index
if os.path.exists(vector_index_file):
    print("Loading pre-built vector index...")
    vector_index = load_data(vector_index_file)
else:
    print("Building vector index...")
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    vector_index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    save_data(vector_index, vector_index_file)

# Create query and chat engines
query_engine = vector_index.as_query_engine(llm=llm)
chat_engine = vector_index.as_chat_engine(chat_mode="react", llm=llm, verbose=False)

# Define tools
tools = [
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="Search",
            description="Useful for reading the Valmiki Ramayana and retrieving storylines."
        )
    ),
    QueryEngineTool(
        query_engine=chat_engine,
        metadata=ToolMetadata(
            name="Chat",
            description="Useful for casual, open-ended inquiries or conversations."
        )
    )
] + get_tools(query_engine)

# Initialize the agent
agent = ReActAgent.from_tools(tools, llm=llm, context=context, verbose=False)

# Retry mechanism for handling queries
def query_with_retry(query: str, max_retries: int=3, wait_time: int=30) -> StreamingAgentChatResponse:
    for attempt in range(max_retries):
        try:
            start_time = datetime.now()
            response = agent.stream_chat(query)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"Query completed in {duration:.2f} seconds.")
            return response
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Error occurred: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception()

# if __name__ == "__main__":
#     while True:
#         q = input("Jai Sri Ram :> ")
#         if q.lower() in ['q', 'quit', 'exit']:
#             print("Goodbye! :<")
#             break
#         response = query_with_retry(q)
#         if response:
#             print(response)
def handle_query(query: str) -> StreamingAgentChatResponse:
    try:
        response = query_with_retry(query)
        return response
    except Exception as e:
        return f"An error occurred: {e}"    

