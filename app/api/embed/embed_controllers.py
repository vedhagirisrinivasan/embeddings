import os

import openai
from app.api.embed.constant import MODEL, TEMPERATURE
from app.extensions import db
from app.models.models import UserEmbeddings
from app.utils.status import status
from config import Config
from dotenv import load_dotenv
from flask_jwt_extended import get_jwt_identity
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.text_splitter import RecursiveCharacterTextSplitter  # split
from langchain.vectorstores.pgvector import PGVector
from langchain_community.document_loaders import (CSVLoader,  # load
                                                  PyMuPDFLoader, TextLoader)
from langchain_community.embeddings import OpenAIEmbeddings  # embed
from langchain_openai import ChatOpenAI

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
connection_string = Config.SQLALCHEMY_DATABASE_URI


def embed_files(data):
    try:
        file = data.get("file")
        collection_name = data.get("collection_name")
        user_id = get_jwt_identity()

        _, file_extension = os.path.splitext(file)
        if file_extension.lower() == ".pdf":
            loader = PyMuPDFLoader(file)
        elif file_extension.lower() == ".csv":
            loader = CSVLoader(file, encoding="utf-8")
        elif file_extension.lower() == ".txt":
            loader = TextLoader(file, encoding="utf-8")
        else:
            data = status(
                status=True,
                body=None,
                message="File type cannot be processed",
                error=None,
            )
            return data, 400
        documents = loader.load()

        # split
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        )
        texts = text_splitter.split_documents(documents)
        # embed
        embeddings = OpenAIEmbeddings()
        text_embeddings = [text.page_content for text in texts]
        embeddings.embed_documents(text_embeddings)
        PGVector.from_documents(
            embedding=embeddings,
            documents=texts,
            collection_name=collection_name,
            connection_string=connection_string,
        )
        user_id = get_jwt_identity()

        collections = UserEmbeddings(user_id=user_id, collection_name=collection_name)
        db.session.add(collections)
        db.session.commit()

        data = (
            status(status=True, body=None, message="EMBEDDED SUCCESSFULLY", error=None),
            200,
        )
        return data, 200
    except Exception as e:
        data = status(status=True, body=None, message=str(e), error=None)
        return data, 500


def prompting(data):
    try:
        query = data.get("query")
        user_id = get_jwt_identity()
        collection = UserEmbeddings.query.filter_by(user_id=user_id).first()
        if collection is None:
            data = status(status=True, body=None, message="NO RESULT FOUND", error=None)
            return data, 404
        collection_name = collection.collection_name

        embeddings = OpenAIEmbeddings()
        vector = PGVector(
            collection_name=collection_name,
            connection_string=connection_string,
            embedding_function=embeddings,
        )

        # retrieve embeddings
        retriever = vector.as_retriever(
            search_kwargs={"k": 4},
        )
        prompt = f"""
            If answer is not found in the response above return the content in the given triplebackticks.

            '''I cannot provide an answer to this query based on the available information.'''
            """
        system_template = (
            prompt
            + """
            human:{question}
            summaries:{summaries}"""
        )
        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
        ]
        messages.append(HumanMessagePromptTemplate.from_template("{question}"))
        prompt = ChatPromptTemplate.from_messages(messages)
        chain_type_kwargs = {"prompt": prompt}
        llm = ChatOpenAI(temperature=TEMPERATURE, model=MODEL)
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs=chain_type_kwargs,
            verbose=True,
            return_source_documents=True,
        )
        response = chain(query)
        response = response["answer"].strip()

        data = (
            status(status=True, body=response, message="RESULT FOUND", error=None),
            200,
        )
        return data, 200
    except Exception as e:
        data = status(status=True, body=None, message=str(e), error=None)
        return data, 500
