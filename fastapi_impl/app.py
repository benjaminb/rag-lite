import base64
import boto3
import json
import os
from fastapi import FastAPI, HTTPException
from langchain_community.document_loaders import TextLoader, PyPDFLoader, BSHTMLLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel
import chromadb


class Event(BaseModel):
    headers: dict
    body: str


"""
Database constants
"""
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


vector_store = Chroma(
    collection_name="general",
    embedding_function=embeddings,
    client=chromadb.PersistentClient(path='/mnt/efs/chroma'),
)
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 200
LOADERS = {
    'txt': TextLoader,
    'pdf': PyPDFLoader,
    'html': BSHTMLLoader,
}

"""
Completion model constants
"""
ENDPOINT_NAME = 'llama-1b-endpoint'
COMPLETION_PARAMETERS = {
    "max_new_tokens": 1000,
    "temperature": 0.2
}
TOP_K = 2
with open('prompt_template.txt', 'r') as file:
    PROMPT_TEMPLATE = file.read()


app = FastAPI()


@app.get("/heartbeat")
async def heartbeat():
    return {
        'statusCode': 200,
        'body': json.dumps('Alive')
    }


@app.post("/ask_question")
async def ask_question(event: Event):

    # Resolve references and prepare prompt
    references = get_top_references(event)
    reference_str = "\n###\n".join(
        reference['content'] for reference in references)

    prompt = PROMPT_TEMPLATE.format(
        query=event.body, references=reference_str)
    payload = {
        "inputs": prompt
    }

    # Invoke the llm endpoint and format the response
    text = get_completion(payload, prompt)
    return {
        'statusCode': 200,
        'body': text,
        'references': json.dumps(references)
    }


@app.post("/ask_question_no_refs")
async def ask_question_no_refs(event: Event):
    prompt = PROMPT_TEMPLATE.format(
        query=event.body, references='')
    payload = {
        "inputs": prompt
    }

    text = get_completion(payload, prompt)
    return {
        'statusCode': 200,
        'body': text,
        'references': json.dumps([])
    }


def get_completion(payload, prompt):
    # Initialize the SageMaker runtime client
    session = boto3.Session(profile_name='default')
    sagemaker_runtime = session.client(
        'sagemaker-runtime', region_name='us-east-1')

    # Invoke the SageMaker endpoint
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType='application/json',
        Body=json.dumps(payload)
    )

    # Format the response
    response_body = json.loads(response['Body'].read().decode())
    completion = response_body[0]['generated_text']
    generated_text = completion.replace(prompt, '').strip()
    return generated_text


def get_top_references(event: Event):
    query = event.body
    # Use 'k' header if provided, else use default
    top_k = event.headers.get('k', TOP_K)

    document_chunks = vector_store.similarity_search(
        query=query,
        k=top_k,
    )

    return [{'content': chunk.page_content,
             'source': chunk.metadata['source'],
             'page': chunk.metadata['page']} for chunk in document_chunks]


@app.post("/add_document")
async def add_document(event: Event):
    file_content = base64.b64decode(event.body)
    filename = event.headers.get('filename')
    filetype = filename.split('.')[-1]

    # Get loader based on file extension
    doc_loader = LOADERS.get(filetype, None)
    if not doc_loader:
        raise HTTPException(
            status_code=400, detail=f'Unsupported file type (unrecognized extension): {filename}')

    # Write out doc, then load from file
    temp_file_path = f'/tmp/{filename}'
    with open(temp_file_path, 'wb') as file:
        file.write(file_content)
    docs = doc_loader(temp_file_path).load()
    os.remove(temp_file_path)

    # Chunk the document
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP)

    chunks = []
    for i, doc in enumerate(docs):
        chunks += [Document(page_content=chunk.page_content,
                            metadata={
                                'source': filename,
                                'page': i + 1,
                            })
                   for chunk in splitter.split_documents([doc])]
    ids = vector_store.add_documents(documents=chunks)

    return {
        'statusCode': 200,
        'body': json.dumps(f'Added {len(chunks)} chunks')
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
