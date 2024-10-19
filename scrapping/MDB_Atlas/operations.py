from scrapping.processing import Processing
from scrapping.models.artist.artist import Artist
from scrapping.MDB_Atlas.connection import ArtworkRepository


class Operation:
    def __init__(self, artist_id: str) -> None:
        self.artist_id = artist_id

    def save_artist_in_DB(self) -> str:
        process = Processing(self.artist_id)
        artist_data = process.get_artist()
        if isinstance(artist_data, Artist):
            ArtworkRepository().save_artist(artist_data)
            return 'Artist saved successfully'
        else:
            return artist_data

    def save_artwork_in_DB(self, artwork_id: str) -> str:
        process = Processing(self.artist_id)
        artwork_data = process.get_artwork(artwork_id)
        ArtworkRepository().save_artwork(artwork_data)
        return 'Artwork saved successfully'

    def save_previews_in_DB(self, quantity: int | str) -> str:
        process = Processing(self.artist_id)
        previews = process.get_previews(quantity)
        ArtworkRepository().save_previews(previews)
        return 'Previews saved successfully'

    def save_artworks_in_DB(self, quantity: int | str) -> str:
        process = Processing(self.artist_id)
        artworks = process.get_artworks(quantity)
        ArtworkRepository().save_artworks(artworks)
        return 'Artworks saved successfully'
