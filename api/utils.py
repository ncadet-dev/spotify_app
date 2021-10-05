def albums_dict_to_artists_list(dictionary):
    """Convert a dictionary of albums into a list of artists."""
    items = dictionary['albums']['items']

    for item in items:
        del item['available_markets']
        del item['images']

    return items
