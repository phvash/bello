from tools import config, connections

username = config.get_username()
if username is None:
    config.set_username(raw_input("Enter a username for Bello"))
print "Welcome to Bello %s" % username

connections.listen(username, host='0.0.0.0')
