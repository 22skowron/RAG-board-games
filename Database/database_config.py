import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

DB_NAME = os.environ.get('DB_NAME')
COLLECTION_NAME = os.environ.get('COLLECTION_NAME')
HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))


def connect_to_cosmosdb(host, port, db_name, collection_name):
    try:
        client_mongodb = MongoClient(
            host=host,
            port=port,
            serverSelectionTimeoutMS=5000
        )
        client_mongodb.admin.command("ping")

        db = client_mongodb[db_name]
        collection = db[collection_name]

        print("MongoDB connection established successfully.")
        return collection

    except Exception as e:
        print(f"Could not connect to MongoDB due to: {e}")
        return None


collection = connect_to_cosmosdb(HOST, PORT, DB_NAME, COLLECTION_NAME)

