from scrapping.MDB_Atlas.operations import Operation


def main():
    operation = Operation('onyricstudio')
    action = 1
    
    match action:
        case 1:
            artist_state = operation.save_artist_in_DB()
            print(artist_state)
        case 2:
            previews_state = operation.save_previews_in_DB('all')
            print(previews_state)
        case 3:
            artwork_state = operation.save_artwork_in_DB('684zWn')
            print(artwork_state)
        case 4:
            artworks_state = operation.save_artworks_in_DB('all')
            print(artworks_state)
        case _:
            print('Option not allowed')

if __name__ == '__main__':
    main()