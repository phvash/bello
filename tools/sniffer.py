import wifi
from nconnections import Sender
import socket
from ping import scan_net

# def get_active_ips():

#     lower_limit, upper_limit = wifi.get_addrs_range(wifi.get_wifi_detail())
#     ip_range = (wifi.generate_ip(lower_limit, upper_limit))
#     active_ips = ip_parser.get_active_ips(ip_range)

#     return active_ips


def get_active_ips():
    lower_limit, upper_limit = wifi.get_addrs_range(wifi.get_wifi_detail())
    ip_range = (wifi.generate_ip(lower_limit, upper_limit))
    network = scan_net(ip_range)
    network.scan()
    return network.active_ips


def get_active_users():
    active_ips = get_active_ips()
    active_users_db = {}
    for address in active_ips:
        try:
            conn = Sender(ip=address, port=9482)
            conn.send('dummy')
            username = conn.receive_reply()
            if username:
                active_users_db[username] = address
            if conn.active:
                conn.end
        except socket.error:
            pass
    return active_users_db
