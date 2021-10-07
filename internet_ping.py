import socket

REMOTE_SERVER = "one.one.one.one"


def is_connected():
    hostname = REMOTE_SERVER
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False


# is_connected(REMOTE_SERVER)
