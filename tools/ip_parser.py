import platform
import os
from threading import Thread
from stack import stack


IPList = stack()


def determine_platform():
    """ Determines the platform on which the program is being run"""
    os_on_system = platform.system()
    if os_on_system == 'Windows':
        ping = 'ping -n 1 '
    else:
        ping = 'ping -c 1 '
    return  ping


def Command_operation(ip_to_use):
    """This determines the whether an ip is alive.
    if it's alive it pushes it into the Stack"""
    ping = determine_platform()
    for ips in ip_to_use:
        pinging = ping + ips
        try:
            reply = os.popen(pinging)
            for lines in reply.readlines():
                if lines.count('ttl'):
                    IPList.push(ips)
                else:
                    pass
        except:
            pass


def get_active_ips(list_of_ips):
    """ This is where each thread is assigned it's task
    and the ips are assigned to each thread"""
    threads = []
    number_Of_Ips = len(list_of_ips)
    number_Of_threads = 5
    number_Of_ips_per_thread = number_Of_Ips// number_Of_threads
    start_of_ip = 0
    for thread in range(number_Of_threads):
        end_of_ip = start_of_ip + number_Of_ips_per_thread
        if end_of_ip > number_Of_Ips:
            end_of_ip = number_Of_Ips
        ip_to_use = (list_of_ips[start_of_ip:end_of_ip],)
        start_of_ip = end_of_ip+1
        thr = Thread(target=Command_operation, args=ip_to_use)
        thr.setDaemon(True)
        thr.start()
        threads.append(thr)
    for td in threads:
        td.join()
    return IPList.get_item()

# For testing the program
if __name__ =="__main__":
    list_of_ip = ['www.google.com','www.github.com','198.123.43.4','www.facebook.com','www.tooxclusive.com','198.123.43.9','www.instagram.com','198.123.43.23','www.mitocw.org']
    y = get_active_ips(list_of_ip)
    print(y)







