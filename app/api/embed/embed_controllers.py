from langchain.text_splitter import RecursiveCharacterTextSplitter   #split
from langchain_community.document_loaders import TextLoader    # load
from langchain_community.embeddings import OpenAIEmbeddings   # embed
from langchain.vectorstores.pgvector import PGVector
from flask_jwt_extended import get_jwt_identity
from app.utils.status import status
from config import Config
from app.extensions import db
from app.models.models import UserEmbeddings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
import os
import openai

load_dotenv()

openai.api_key  = os.getenv('OPENAI_API_KEY')
connection_string = Config.SQLALCHEMY_DATABASE_URI

def embed_files(data):
    file = data.get("file")
    collection_name = data.get("collection_name")
    user_id = get_jwt_identity()
    # load
    loader = TextLoader(file, encoding='utf-8')
    documents = loader.load()

    # split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    # embed
    embeddings = OpenAIEmbeddings()
    text_embeddings = [text.page_content for text in texts]
    vector = embeddings.embed_documents(text_embeddings)
    db_embed = PGVector.from_documents(embedding=embeddings, documents=texts, collection_name=collection_name, connection_string=connection_string)
    user_id = get_jwt_identity()

    collections = UserEmbeddings(user_id=user_id,collection_name=collection_name)
    db.session.add(collections)
    db.session.commit()

    
    data = (status(status=True, body=None, message="EMBEDDED SUCCESSFULLY", error=None), 200)

    return data, 200
        

def prompting(data):
    query = data.get("query")
    user_id = get_jwt_identity()
    collection = UserEmbeddings.query.filter_by(user_id=user_id).first()
    collection_name = collection.collection_name
    embeddings=OpenAIEmbeddings()
    vector = PGVector(
        collection_name=collection_name,
        connection_string=connection_string,
        embedding_function=embeddings,
    )
    retriever = vector.as_retriever(
        search_kwargs={"k": 1}
        )
    llm = ChatOpenAI(temperature = 0.2, model = 'gpt-3.5-turbo-16k')
    qa_stuff = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        verbose=True,
        return_source_documents=True
    )   
    
    response = qa_stuff.invoke(query)
    values = response['source_documents'][0]
    source_documents = response['answer']
    if source_documents.startswith("There is no information provided about"):
        data = (status(status=True, body=None, message="NO RESULT FOUND", error=None), 200)
        return data, 404
    else:
        data = (status(status=True, body=source_documents, message="RESULT FOUND", error=None), 200)
        return data, 200
