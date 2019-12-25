import socket

REMOTE_SERVER = "www.google.com"


def check_connectivity(hostname=REMOTE_SERVER):
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False
