from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
import argparse

DATA_PATH = args.folder
DB_FAISS_PATH = 'vectorstore/db_faiss'  #Embedding created will go to 

# Create vector database
def create_vector_db():
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()

    #Split it in chunks EXPLAIN WHAT IS A CHUNK 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # Creare embeddings based on MINI - Sentence transformers
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parser')
    parser.add_argument('--folder', help='folder')
    # Parse the command-line arguments
    args = parser.parse_args()

    create_vector_db()