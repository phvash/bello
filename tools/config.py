import shelve


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
