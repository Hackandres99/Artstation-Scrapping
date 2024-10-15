from artstation_scraper.processing import Processing
# from artstation_scraper.MDB_connection import ArtworkRepository


def main():
    artist = 'tsmith3d'
    process = Processing(artist)
    print(process.get_artist())
    print(process.get_artwork(27))
    # print(process.get_artworks())

    # ArtworkRepository().save_artwork(artwork)
    # print(f'Artwork {i + 1} saved successfully.')


if __name__ == '__main__':
    main()
