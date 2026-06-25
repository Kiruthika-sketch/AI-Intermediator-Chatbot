import chromadb
import ollama
import uuid

# Create/Open ChromaDB
client = chromadb.PersistentClient(path="backend/chroma_db")

collection = client.get_or_create_collection(
    name="pdf_documents"
)


def store_chunks(chunks, filename):
    """
    Store all chunks of a PDF.
    Existing PDFs are NOT deleted.
    """

    for i, chunk in enumerate(chunks):

        response = ollama.embed(
            model="nomic-embed-text",
            input=chunk
        )

        embedding = response["embeddings"][0]

        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[
                {
                    "filename": filename,
                    "chunk": i
                }
            ]
        )


def search_chunks(question, top_k=8):
    """
    Search across ALL uploaded PDFs.
    """

    response = ollama.embed(
        model="nomic-embed-text",
        input=question
    )

    question_embedding = response["embeddings"][0]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    return results["documents"][0]


def list_pdfs():
    """
    Return list of uploaded PDFs.
    """

    data = collection.get(
        include=["metadatas"]
    )

    pdfs = set()

    for meta in data["metadatas"]:

        pdfs.add(meta["filename"])

    return sorted(list(pdfs))


def delete_pdf(filename):
    """
    Delete one PDF only.
    """

    data = collection.get(include=["metadatas"])

    ids = []

    for i, meta in enumerate(data["metadatas"]):

        if meta is not None and meta.get("filename") == filename:

            ids.append(data["ids"][i])

    if ids:

        collection.delete(ids=ids)