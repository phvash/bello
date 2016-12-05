''' okay the idea is simple

we have a host () and a client bundled in the app

sniffer:

    - get the list of all devices present
    - determines if the device is accepting bello connections
      ( by attempting to connect to the host-side of bello as a dummie client)
      (if connection successful returns the saved USERNAME for the device)

    * depends on the client script

the host:

    - listens for incoming connections on bello port
    - if connection mode is set to 'dummie' returns the username, ends connection
    - else starts a life stream socket

the client:
    - attempts to establish a bello connection to a host in dummie mode or chat mode

 '''