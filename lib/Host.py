import socket
import getpass

def getHostIp():
    """
    Get the local IP address of the host.
    :return: str
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def getUser():
    """
    Get the current username.
    :return: str
    """
    return getpass.getuser()

def getHostName():
    """
    Get the hostname of the host.
    :return: str
    """
    return socket.gethostname()
