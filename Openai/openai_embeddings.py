from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client_openai = OpenAI()


def generate_embedding(query):
    try:
        response = client_openai.embeddings.create(
            model="text-embedding-ada-002",
            input=query,
            timeout=10
        )
        embedding = response.data[0].embedding
        print(f"✅ Successfully generated the embedding!")
        return embedding

    except Exception as e:
        print(f"❌ Error generating the embedding: {e}")
        return None
# response.data - a list of embedding objects - each has an embedding vector under "embedding" property
