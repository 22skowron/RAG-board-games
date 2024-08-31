from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def get_top_n_documents(user_query_embedding, documents, top_n=3):
    # print(f"* user_query_embedding shape: {np.array([user_query_embedding]).shape}")

    doc_embeddings = np.array([doc['embedding'] for doc in documents])
    # print(f"* doc_embeddings shape: {doc_embeddings.shape}")

    # Compute cosine similarity
    similarities = cosine_similarity(np.array([user_query_embedding]), doc_embeddings)
    # print(f"* similarities shape: {similarities.shape}\n")

    # Get the indices of the top n similarities
    top_n_indices = similarities.argsort()[0, -top_n:][::-1]
    # print(f"* top_n_indices : {top_n_indices}")
    print(f"* top_n_similarities : {[similarities[0, i] for i in top_n_indices]}\n")

    top_n_documents = [documents[i] for i in top_n_indices]
    return top_n_documents

