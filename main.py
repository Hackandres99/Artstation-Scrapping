from scrapping.MDB_Atlas.operations import Operation


def main():
    operation = Operation('onyricstudio')
    # artist_state = operation.save_artist_in_DB()
    # print(artist_state)
    # previews_state = operation.save_previews_in_DB('all')
    # print(previews_state)
    # artwork_state = operation.save_artwork_in_DB('684zWn')
    # print(artwork_state)
    artworks_state = operation.save_artworks_in_DB('all')
    print(artworks_state)

if __name__ == '__main__':
    main()