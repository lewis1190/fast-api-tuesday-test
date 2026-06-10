import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import json

# Initialize Firebase
# For local development, use the service account key file
# For Heroku, use the FIREBASE_CREDENTIALS environment variable
if os.getenv("FIREBASE_CREDENTIALS"):
    # Heroku deployment: read credentials from environment variable
    firebase_credentials = json.loads(os.getenv("FIREBASE_CREDENTIALS"))
    cred = credentials.Certificate(firebase_credentials)
else:
    # Local development: read from file
    cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred)

db = firestore.client()


def add_data(collection: str, data: dict):
    """Add a document to a Firestore collection"""
    return db.collection(collection).add(data)


def get_data(collection: str):
    """Retrieve all documents from a Firestore collection"""
    docs = db.collection(collection).stream()
    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id  # Include document ID
        data.append(doc_data)
    return data


def seed_data():
    """Seed the database with initial data"""
    sample_data = [
        {"name": "Item 1", "description": "This is item 1"},
        {"name": "Item 2", "description": "This is item 2"},
        {"name": "Item 3", "description": "This is item 3"},
    ]

    for data in sample_data:
        add_data("data", data)

    return {"message": f"Seeded {len(sample_data)} items"}


def verify_token(token: str):
    """Verify a Firebase ID token and return the decoded token"""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise Exception(f"Invalid token: {str(e)}")
