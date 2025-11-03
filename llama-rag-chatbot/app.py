import streamlit as st
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredExcelLoader,
    Docx2txtLoader,
    UnstructuredWordDocumentLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from sentence_transformers import SentenceTransformer, util
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.chains import create_history_aware_retriever
from langchain_huggingface import HuggingFaceEmbeddings
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import tempfile
import os
import pandas as pd
import pickle
import io
from typing import List

# Constants
GOOGLE_DRIVE_FOLDER_ID = "1_EUeDEC4ymbsjNFGjIXSvBSbzg4FWbcT"  # Replace with your folder ID
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# UI Templates
bot_template = '''
<div style="display: flex; align-items: center; margin-bottom: 10px;">
    <div style="flex-shrink: 0; margin-right: 10px;">
        <img src="https://uxwing.com/wp-content/themes/uxwing/download/communication-chat-call/answer-icon.png" 
             style="max-height: 50px; max-width: 50px; border-radius: 50%; object-fit: cover;">
    </div>
    <div style="background-color: #e0e0e0; color: #333; padding: 10px; border-radius: 10px; max-width: 75%; word-wrap: break-word; overflow-wrap: break-word;">
        {msg}
    </div>
</div>
'''

user_template = '''
<div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: flex-end;">
    <div style="background-color: #007bff; color: white; padding: 10px; border-radius: 10px; max-width: 75%; word-wrap: break-word; overflow-wrap: break-word;">
        {msg}
    </div>
    <div style="flex-shrink: 0; margin-left: 10px;">
        <img src="https://cdn.iconscout.com/icon/free/png-512/free-q-characters-character-alphabet-letter-36051.png?f=webp&w=512" 
             style="max-height: 50px; max-width: 50px; border-radius: 50%; object-fit: cover;">
    </div>
</div>
'''

button_style = """
<style>
    .small-button {
        display: inline-block;
        padding: 5px 10px;
        font-size: 12px;
        color: white;
        background-color: #007bff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-right: 5px;
    }
    .small-button:hover {
        background-color: #0056b3;
    }
</style>
"""

# Google Drive Functions
def authenticate_google_drive():
    """Authenticate with Google Drive."""
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_files_from_folder(service, folder_id: str) -> List[dict]:
    """Get all files from a specific Google Drive folder."""
    results = []
    page_token = None
    
    while True:
        try:
            query = f"'{folder_id}' in parents and trashed = false"
            files = service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType)',
                pageToken=page_token
            ).execute()
            
            results.extend(files.get('files', []))
            page_token = files.get('nextPageToken')
            
            if not page_token:
                break
                
        except Exception as e:
            st.error(f"Error retrieving files: {str(e)}")
            break
    
    return results

def load_document(file_path, file_extension):
    """Load document based on file extension."""
    try:
        if file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_extension == '.txt':
            loader = TextLoader(file_path)
        elif file_extension == '.csv':
            loader = CSVLoader(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            loader = UnstructuredExcelLoader(file_path, mode="elements")
        elif file_extension == '.docx':
            loader = Docx2txtLoader(file_path)
        elif file_extension == '.doc':
            loader = UnstructuredWordDocumentLoader(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
        
        return loader.load()
    except Exception as e:
        st.error(f"Error loading file {file_path}: {str(e)}")
        return []

def download_and_load_file(service, file_id: str, file_name: str) -> List:
    """Download and load a file from Google Drive."""
    try:
        request = service.files().get_media(fileId=file_id)
        file_handle = io.BytesIO()
        downloader = MediaIoBaseDownload(file_handle, request)
        done = False
        
        while not done:
            status, done = downloader.next_chunk()
        
        file_extension = os.path.splitext(file_name)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(file_handle.getvalue())
            temp_path = temp_file.name
        
        documents = load_document(temp_path, file_extension)
        os.unlink(temp_path)
        
        return documents
    
    except Exception as e:
        st.error(f"Error downloading file {file_name}: {str(e)}")
        return []

def process_drive_files():
    """Process all files from the specified Google Drive folder."""
    try:
        creds = authenticate_google_drive()
        service = build('drive', 'v3', credentials=creds)
        
        files = get_files_from_folder(service, GOOGLE_DRIVE_FOLDER_ID)
        
        if not files:
            st.error("No files found in the specified Google Drive folder")
            return None
        
        st.info(f"Found {len(files)} files in Google Drive folder")
        
        split_docs = prepare_and_split_docs_from_drive(service, files)
        return split_docs
        
    except Exception as e:
        st.error(f"Error connecting to Google Drive: {str(e)}")
        return None

def prepare_and_split_docs_from_drive(service, files):
    """Prepare and split documents from Google Drive files."""
    split_docs = []
    
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512,  #512
        chunk_overlap=256, #256
        disallowed_special=(),
        separators=["\n\n", "\n", " "]
       
    )
    
    progress_bar = st.progress(0)
    for idx, file in enumerate(files):
        try:
            documents = download_and_load_file(service, file['id'], file['name'])
            
            if documents:
                split_docs.extend(splitter.split_documents(documents))
            
            progress_bar.progress((idx + 1) / len(files))
            
        except Exception as e:
            st.error(f"Error processing {file['name']}: {str(e)}")
            continue
    
    progress_bar.empty()
    return split_docs


#Vector Database Functions
def ingest_into_vectordb(split_docs):
    """Create and save vector database from documents."""
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db = FAISS.from_documents(split_docs, embeddings)
    DB_FAISS_PATH = 'vectorstore/db_faiss'
    db.save_local(DB_FAISS_PATH)
    return db

def get_conversation_chain(retriever):
    """
    Create a conversation chain with document retriever and chat history awareness.
    
    Args:
        retriever: Document retriever instance
    Returns:
        RunnableWithMessageHistory: Configured conversation chain
    """
    llm = OllamaLLM(model="llama3", temperature=0)
    #llm = OllamaLLM(model="mistral", temperature=0)
    
    # System prompt for contextualizing questions based on chat history
    contextualize_q_system_prompt = """
    You are a precise and focused assistant. Your task is to:
    1. Analyze the chat history and current question carefully.
    2. Use only the information provided in the documents to construct a direct and factual response.
    3. Maintain context from the chat history when relevant.
    4. Do not speculate beyond the provided information.

    Important guidelines:
    - Provide specific, concrete answers.
    - Stay within the scope of the documents.
    - Maintain a professional and informative tone.
    - Do not ask follow-up questions.
    - Do not rephrase the user's question.
    """

    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    history_aware_retriever = create_history_aware_retriever(
        llm, 
        retriever, 
        contextualize_q_prompt
    )

    # Main system prompt for generating responses
    system_prompt = """
    You are a knowledgeable and concise customer service assistant. Your responses should:
    1. Be highly relevant to the user's query.
    2. Draw exclusively from the provided documents: {context}.
    3. Be between 2-5 sentences (maximum 100 words).
    4. Focus on key information and main points.
    5. Use clear and direct language.

    Important guidelines:
    - Provide complete, self-contained answers.
    - Include specific details when relevant.
    - Maintain a friendly and professional tone.
    - Do not ask questions or suggest options.
    - Do not acknowledge limitations or apologize.
    """

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    # Session history management
    store = {}
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    return RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )


def calculate_similarity_score(answer: str, context_docs: list) -> float:
    """Calculate similarity between answer and context documents."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    context_docs = [doc.page_content for doc in context_docs]
    
    answer_embedding = model.encode(answer, convert_to_tensor=True)
    context_embeddings = model.encode(context_docs, convert_to_tensor=True)
    
    similarities = util.pytorch_cos_sim(answer_embedding, context_embeddings)
    return similarities.max().item()

# Main Application
def main():
    st.title("📚 Document Chat with Google Drive")
    st.markdown(button_style, unsafe_allow_html=True)

    # Initialize session states
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'show_docs' not in st.session_state:
        st.session_state.show_docs = {}
    if 'similarity_scores' not in st.session_state:
        st.session_state.similarity_scores = {}
    if 'docs_processed' not in st.session_state:
        st.session_state.docs_processed = False

    # Process documents if not already done
    if not st.session_state.docs_processed:
        with st.spinner("Processing documents from Google Drive..."):
            split_docs = process_drive_files()
            
            if split_docs:
                vector_db = ingest_into_vectordb(split_docs)
                retriever = vector_db.as_retriever()
                st.session_state.conversational_chain = get_conversation_chain(retriever)
                st.session_state.docs_processed = True
                st.success("✅ Documents processed successfully!")

    # Chat interface
    user_input = st.text_input("Ask a question about your documents:", placeholder="Type your question here...")

    if st.button("Submit"):
        if user_input and hasattr(st.session_state, 'conversational_chain'):
            with st.spinner("Generating response..."):
                session_id = "abc123"
                response = st.session_state.conversational_chain.invoke(
                    {"input": user_input},
                    config={"configurable": {"session_id": session_id}}
                )
                context_docs = response.get('context', [])
                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": response['answer'],
                    "context_docs": context_docs
                })


    # Display chat history
    for index, message in enumerate(st.session_state.chat_history):
      # User message
      st.markdown(user_template.format(msg=message['user']), unsafe_allow_html=True)

      # Bot message
      st.markdown(bot_template.format(msg=message['bot']), unsafe_allow_html=True)

      # Ensure 'similarity_score' and 'show_docs' keys are initialized
      if f"similarity_score_{index}" not in st.session_state:
        st.session_state[f"similarity_score_{index}"] = None
      if f"show_docs_{index}" not in st.session_state:
        st.session_state[f"show_docs_{index}"] = False

      # Control buttons
      cols = st.columns([1, 1])

      with cols[0]:
        if st.button(f"📄 Show/Hide Sources", key=f"toggle_{index}"):
            st.session_state[f"show_docs_{index}"] = not st.session_state[f"show_docs_{index}"]

      with cols[1]:
        if st.button(f"🎯 Calculate Relevancy", key=f"relevancy_{index}"):
            if st.session_state[f"similarity_score_{index}"] is None:
                score = calculate_similarity_score(message['bot'], message['context_docs'])
                st.session_state[f"similarity_score_{index}"] = score

    
        # Show source documents if enabled
        if st.session_state[f"show_docs_{index}"]:
            with st.expander("Source Documents"):
                for doc in message.get('context_docs', []):
                    st.markdown(f"**Source:** {doc.metadata['source']}")
                    st.markdown(doc.page_content)

        # Display similarity score if calculated
        if st.session_state[f"similarity_score_{index}"] is not None:
            score = st.session_state[f"similarity_score_{index}"]
            score_color = "green" if score > 0.7 else "orange" if score > 0.5 else "red"
            st.markdown(f"Relevancy Score: <span style='color:{score_color}'>{score:.2f}</span>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
