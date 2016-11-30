import shelve, os


preferences = shelve.open('settings')

# def startup():
#
#     if os.path.exists('settings'):

def get_username():

    try:
        username = preferences['username']
    except:
        username = raw_input('Kindly enter a username for Bello: ')
        preferences['username'] = username

    return username