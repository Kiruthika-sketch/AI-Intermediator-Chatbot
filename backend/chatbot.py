import ollama

conversation = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant. Answer the user's questions using the provided document context whenever available."
    }
]


def chat_with_ai(user_message):

    conversation.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    response = ollama.chat(
        model="llama3.2:1b",
        messages=conversation
    )

    reply = response["message"]["content"]

    conversation.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    return reply


def chat_with_pdf(context, question):

    prompt = f"""
Use ONLY the information from the document below.

Document:
{context}

Question:
{question}

If the answer is not in the document, say:
"I couldn't find that information in the uploaded PDF."
"""

    response = ollama.chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]