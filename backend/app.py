from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from backend.pdf_reader import extract_text
from backend.text_splitter import split_text

from backend.chatbot import (
    chat_with_ai,
    chat_with_pdf
)

from backend.database import (
    create_database,
    get_chat_history
)

from backend.vector_store import (
    store_chunks,
    search_chunks,
    list_pdfs,
    delete_pdf
)

app = FastAPI()

create_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():

    return {
        "message": "AI Intermediator Chatbot API is running!"
    }


@app.get("/history")
def history():

    return {
        "history": get_chat_history()
    }


# -----------------------------
# Upload PDF
# -----------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    os.makedirs("backend/uploads", exist_ok=True)

    file_path = f"backend/uploads/{file.filename}"

    with open(file_path, "wb") as buffer:

        buffer.write(await file.read())

    pdf_text = extract_text(file_path)

    if len(pdf_text.strip()) == 0:

        return {
            "message": "No text found in PDF."
        }

    chunks = split_text(pdf_text)

    store_chunks(
        chunks,
        file.filename
    )

    return {

        "message": "PDF uploaded successfully!",

        "filename": file.filename,

        "characters": len(pdf_text),

        "chunks": len(chunks)

    }


# -----------------------------
# Ask PDF
# -----------------------------
@app.post("/ask-pdf")
async def ask_pdf(request: ChatRequest):

    try:

        chunks = search_chunks(request.message)

        if not chunks:

            return {

                "reply": "I couldn't find any relevant information in the uploaded PDFs."

            }

        context = "\n\n".join(chunks)

        answer = chat_with_pdf(

            context,

            request.message

        )

        return {

            "reply": answer

        }

    except Exception as e:

        print(e)

        return {

            "error": str(e)

        }


# -----------------------------
# Normal Chat
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    answer = chat_with_ai(
        request.message
    )

    return {

        "reply": answer

    }


# -----------------------------
# List Uploaded PDFs
# -----------------------------
@app.get("/pdfs")
def get_pdfs():

    return {

        "pdfs": list_pdfs()

    }


# -----------------------------
# Delete One PDF
# -----------------------------
@app.delete("/delete-pdf/{filename}")
def remove_pdf(filename: str):

    delete_pdf(filename)

    pdf_path = f"backend/uploads/{filename}"

    if os.path.exists(pdf_path):

        os.remove(pdf_path)

    return {

        "message": f"{filename} deleted successfully."

    }