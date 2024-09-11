from flask import Flask, request, jsonify
from Openai.openai_embeddings import generate_embedding
from Openai.openai_conversation import get_ai_answer, construct_prompt
from Database.database_queries import load_documents
from top_n_documents import get_top_n_documents
from pprint import pprint

app = Flask(__name__)
chat_history = []


def update_chat_history(user_query, ai_answer):
    chat_history.append({"role": "user", "content": user_query})
    chat_history.append({"role": "assistant", "content": ai_answer})

    # Ensure chat history has a maximum of 20 messages
    while len(chat_history) > 20:
        chat_history.pop(0)
        chat_history.pop(0)


@app.post('/ai_assistant')
def get_ai_response():
    try:
        data = request.get_json()

        user_query = data.get('user_query')
        if not user_query:
            return jsonify({'message': f'❌ Missing user query.'}), 400

        # Embed user query
        user_query_embedding = generate_embedding(user_query)
        if not user_query_embedding:
            return jsonify({'message': f'❌ Failed to generate an embedding.'}), 400

        # Load documents
        documents = load_documents()
        if not documents:
            return jsonify({'message': f'❌ Failed to load documents.'}), 400

        # Retrieve most relevant documents
        top_n_documents = get_top_n_documents(user_query_embedding, documents)

        # Construct the prompt and get AI response
        prompt = construct_prompt(user_query, top_n_documents, chat_history)
        ai_answer = get_ai_answer(prompt)
        if not ai_answer:
            return jsonify({'message': f'❌ Failed to generate Ai response.'}), 400

        update_chat_history(user_query, ai_answer)

        print(f'CHAT HISTORY LENGTH: {len(chat_history)}\n')
        print(f'AI ANSWER:\n{ai_answer}\n')

        return jsonify({'ai_answer': ai_answer}), 200

    except Exception as e:
        print(f'❌ An error occurred during processing the request: {e} ❌')
        return jsonify({'message': f'❌ An error occurred during processing the request: {e}.'}), 400


if __name__ == '__main__':
    app.run(port=5000, debug=True)
