import os
import torch

from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from config import config as config

collection = None
retriever = None
embeddings = None

def pineconedb_init():
    global collection, retriever, embeddings
    
    #embeddings
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_name = config.get_database_config()['embedding_model'] #"BAAI/bge-small-en-v1.5"
    model_kwargs = {'device': device}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    
    #DB
    #os.environ['PINECONE_API_KEY'] = ''
    index_name = config.get_database_config()['environment']['index_name'] #"ai-doc"
    VectorStore = PineconeVectorStore(embedding = embeddings, index_name = index_name)
    retriever = VectorStore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 5, "score_threshold": 0.5})
    
pineconedb_init()