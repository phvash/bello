import subprocess
import os
import exceptions


def get_wifi_detail():

    if 'linux' in os.sys.platform:
        command = 'ifconfig'
    elif 'Windows' in os.sys.platform:
        command = 'ipconfig'
    else:
        return "Exception"

    raw_details = subprocess.check_output([command])

    try:
        response = [addrs[addrs.find(':') + 1:]
                    for addrs in
                     [line[line.find('inet') + 1:]
                     for line in raw_details.split('\n')
                     if 'inet addr' in line and '127' not in line][0].split(' ')

                    if addrs[addrs.find(':') + 1:].replace('.', '').isdigit()]

        return response
    except:
        raise exceptions.ConnectionError("Please connect to a network")


def get_addrs_range(wifi_detail_list):

    me, bcast, mask = wifi_detail_list

    upper_limit = expand_addrs(bcast)

    # GET LOWER LIMIT

    bcast_list = expand_addrs(bcast, aslist=True)
    lower_limit_list = []

    for bcast_octect in bcast_list[:-1]:
        corresponding_mask_octect = mask.split('.')[bcast_list.index(bcast_octect)]
        if corresponding_mask_octect == '255':
            lower_limit_list.append(bcast_octect)
        else:
            lower_limit_list.append('000')
    lower_limit_list.append('001')

    lower_limit = ''.join(lower_limit_list)

    return int(lower_limit), int(upper_limit)


def expand_addrs(ip, aslist=False):

    ip_octects = ip.split('.')
    for octect in ip_octects:
        if len(octect) < 3:
            new_octect = '0' * (3 - len(octect)) + octect
            ip_octects[ip_octects.index(octect)] = new_octect

    expanded_addrs = ''.join(ip_octects)

    if aslist:
        return ip_octects
    else:
        return expanded_addrs


def generate_ip(lower_limit, upper_limit):

    return [reformat_addrs(ip) for ip in range(lower_limit, upper_limit)]


# split in group of 3s
# strip leading zero
# join the groups with '.'
# 192168042001 - 192.168.42.1
def reformat_addrs(ip):

    ip = str(ip)

    # int() removes leading zero in the ip address so we have to add it back

    if len(ip) < 12:
        ip = '0' * (12 - len(ip)) + ip

    octects_list = [ip[i:i+3] for i in range(0, len(ip), 3)]
    for octect in octects_list:
        while True:
            if octect.startswith('0') and len(octect) != 1:
                new_octect = octect[1:]
                octects_list[octects_list.index(octect)] = new_octect
                octect = new_octect
            else:
                break
    return '.'.join(octects_list)


def parse_ping_response(response):

    pass


def ping(address):

    print address.strip("'")
    ping_stat = subprocess.check_output(['ping -c 1 ' + address], shell=True)

    print ping_stat

if __name__ == '__main__':
    lower_limit, upper_limit = get_addrs_range(get_wifi_detail())
    print generate_ip(lower_limit, upper_limit)
    # ping('10.201.0.67')

