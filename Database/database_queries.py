from .database_config import collection


def load_documents():
    try:
        documents = list(collection.find())
        return documents

    except Exception as e:
        print(f'❌ An error occurred during loading the documents. Error: {e} ❌')
        return None


