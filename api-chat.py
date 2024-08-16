from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from llama_index.core.postprocessor import SentenceTransformerRerank
import os

app = FastAPI()

index = None
chat_engine = None

@app.on_event("startup")
async def lifespan():
    global index, chat_engine
    Settings.llm = ChatOllama(model="gemma2", keep_alive="3h", max_tokens=512, temperature=0)
    Settings.embed_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small", model_kwargs={'device': 'cpu'})


    db_path = "./db-multie5-index-final"
    if os.path.exists(db_path):
        storage_context = StorageContext.from_defaults(persist_dir=db_path)
        index = load_index_from_storage(storage_context)
    else:
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        index = VectorStoreIndex.from_documents(docs)
        index.storage_context.persist(persist_dir=db_path)
    
    st_reranker = SentenceTransformerRerank(top_n=3, model="cross-encoder/ms-marco-MiniLM-L-6-v2")
    chat_engine = index.as_chat_engine(chat_mode="context", verbose=True, node_postprocessors=[st_reranker])

@app.post("/chat")
async def chat_endpoint(request: Request):
    request_data = await request.json()
    prompt = request_data.get("prompt", "")

    if not prompt:
        return JSONResponse(content={"error": "No prompt provided"}, status_code=400)

    response_stream = chat_engine.stream_chat(prompt)
    response = "".join([chunk for chunk in response_stream.response_gen])

    return JSONResponse(content={"response": response})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)