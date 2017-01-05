import shelve
preferences = shelve.open('settings')


def get_username():
    try:
        username = preferences['username']
        return username
    except KeyError:
        return None


def set_username(name):
    preferences['username'] = name
