import shelve
<<<<<<< HEAD


class Details:
    def __init__(self):
        self.username = self.get_username()

    @staticmethod
    def get_username():
        preferences = shelve.open('settings')
        try:
            username = preferences['username']
            return username
        except KeyError:
            return None
        finally:
            preferences.close()

    @staticmethod
    def set_username(name):
        preferences = shelve.open('settings')
        preferences['username'] = name
        preferences.close()
=======
preferences = shelve.open('settings')


def get_username():
    try:
        username = preferences['username']
        return username
    except KeyError:
        return None


def set_username(name):
    preferences['username'] = name
>>>>>>> 5b4c03d89f1d30f77450e6e0bd3cbb4cdade8d83
