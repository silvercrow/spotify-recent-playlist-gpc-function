import os

from flask import escape
import functions_framework
import yaml
from pathlib import Path
import random
from database import MongoDBConnection


# Set up MongoDB connection
connection_string = os.environ.get("_DB_STRING")
mongo_database = os.environ.get("_DB_NAME")

# Local development
path = Path(__file__).parent / "./.env.yaml"
environment = os.environ.get("ENV")
if environment == "dev":
    with path.open() as file:
        env = yaml.safe_load(file)
        connection_string = env.get("_DB_STRING")
        mongo_database = env.get("_DB_NAME")

# Create an instance of MongoDBConnection
mongo_connection = MongoDBConnection(connection_string, mongo_database)



@functions_framework.http
def recent_playlist(request):
    try:
        # Connect to MongoDB
        db = mongo_connection.connect()
        if db is not None:
            random_integer = random.randint(1, 100)


            # Specify the condition to find the document you want to update
            filter_criteria = { 
                "settings": "authorization"
            }
            # Specify the update operation
            update_operation = {
                '$set': {
                    # Update the specific field you're interested in
                    'token': random_integer
                }
            }

            # Use update_one to update a single document
            result = db.spotify.update_one(filter_criteria, update_operation)

            # Document not found, create a new one
            if result.matched_count == 0:
                new_document = {
                    "settings": "authorization",
                    "token": random.randint(1, 100)
                }
                db.spotify.insert_one(new_document)
                print("New document created.")

            print(f"{result.matched_count} document(s) matched the filter criteria.")
            print(f"{result.modified_count} document(s) were modified.")


            # Example: Returning a response
            return f"{result.modified_count} document(s) were modified."

    finally:
        # Disconnect from MongoDB after operations
        mongo_connection.disconnect()
