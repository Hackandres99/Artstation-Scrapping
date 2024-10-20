from .MDB_Atlas.operations import Operation
import yaml


def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def run_action(config):
    data = dict()
    heads = ['artist', 'action', 'previews', 'artworks', 'artwork']
    [data.update({head: config[head]}) for head in heads]

    operation = Operation(data['artist'])
    if str(data['action']).isdigit():
        match data['action']:
            case 1:
                artist_state = operation.save_artist_in_DB()
                print(artist_state)
            case 2:
                previews_state = operation.save_previews_in_DB(
                    data['previews']
                )
                print(previews_state)
            case 3:
                artwork_state = operation.save_artwork_in_DB(
                    data['artwork']
                )
                print(artwork_state)
            case 4:
                artworks_state = operation.save_artworks_in_DB(
                    data['artworks']
                )
                print(artworks_state)
            case _:
                print('Option not allowed')
    else:
        print('Action should be a number')
