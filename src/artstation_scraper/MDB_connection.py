import os
from dotenv import load_dotenv
from dataclasses import asdict
from .models.project.artwork import Artwork
from pymongo import MongoClient


class ArtworkRepository:
    def __init__(self) -> None:
        load_dotenv()

        username = os.getenv('MONGODB_USERNAME')
        password = os.getenv('MONGODB_PASSWORD')
        host = os.getenv('MONGODB_HOST')
        port = int(os.getenv('MONGODB_PORT', 27017))
        database = os.getenv('MONGODB_DATABASE')

        connection_string = f"mongodb+srv://{username}:{password}@{host}/"

        self.client = MongoClient(connection_string, port=port)
        self.db = self.client[database]
        self.collection = self.db.artwork

    def save_artwork(self, artwork: Artwork):
        artwork_data = asdict(artwork)
        self.collection.insert_one(artwork_data)

    def get_Artworks(self):
        artworks = self.collection.find({})
        return artworks
