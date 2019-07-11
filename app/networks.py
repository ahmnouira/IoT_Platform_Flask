import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except ConnectionError:
        print("check your connection -> DATABASE will be localhost")
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip
















