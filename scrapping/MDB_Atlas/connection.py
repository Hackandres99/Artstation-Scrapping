import os
from dotenv import load_dotenv
from dataclasses import asdict
from ..models.project.artwork import Artwork
from ..models.artist.artist import Artist
from ..models.artist.artwork_preview import Preview
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
        self.artwork_collection = self.db.artwork
        self.artist_collection = self.db.artist
        self.preview_collection = self.db.preview

    def save_artist(self, artist: Artist):
        artist_data = asdict(artist)
        self.artist_collection.insert_one(artist_data)

    def save_artwork(self, artwork: Artwork):
        artwork_data = asdict(artwork)
        self.artwork_collection.insert_one(artwork_data)

    def save_artworks(self, artworks: list[Artwork]):
        artworks_data = [asdict(artwork) for artwork in artworks]
        self.artwork_collection.insert_many(artworks_data)

    def save_previews(self, previews: list[Preview]):
        previews_data = [asdict(preview) for preview in previews]
        self.preview_collection.insert_many(previews_data)
