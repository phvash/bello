import os, re, threading

received_packages = re.compile(r"(\d) received")

class ip_check(threading.Thread):
   def __init__ (self,ip):
      threading.Thread.__init__(self)
      self.ip = ip
      self.__successful_pings = -1
      self.active = False


   def run(self):
      ping_out = os.popen("ping -q -c2 "+self.ip,"r")
      while True:
        line = ping_out.readline()
        if not line: break
        n_received = re.findall(received_packages,line)
        if n_received:
          self.__successful_pings = int(n_received[0])
        if self.__successful_pings > 0:
          self.active = True
          

class scan_net():


  def __init__(self, ip_range):
    self.ip_range = ip_range
    self.check_results = []
    self.active_ips = []

  def scan(self):
    self.ip_threads = []
    # start thread to handle pinging
    for ip in self.ip_range:
      ip_thread = ip_check(ip)
      self.ip_threads.append(ip_thread)
      ip_thread.start()
    # get respond from each thread
    for ip_thread in self.ip_threads:
      ip_thread.join() # wait till the thread exits
      if ip_thread.active:
        self.active_ips.append(ip_thread.ip)


if __name__ == '__main__':
  test_range = ["192.168.43." + str(suffix) for suffix in range(1,255)]
  test_obj = scan_net(test_range)
  test_obj.scan()
  print test_obj.active_ips