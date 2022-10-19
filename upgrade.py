import logging
import paramiko
import ntpath
from datetime import datetime
import threading


maps_list = [['172.16.0.10', 22, 'root', 'root', '172.16.1.20'],
             ['172.16.0.11', 22, 'root', 'root', '172.16.1.21']]


class SystemUpgrade:
    def __init__(self):
        log: None
        ssh: None
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self.log_file = logging.FileHandler('log.systemUpgrade.log', mode='w')
        self.log_file.setFormatter(logging.Formatter('[%(asctime)s]: [%(name)s]: [%(levelname)s]: %(message)s'))
        self.log.addHandler(self.log_file)
        self.log.info("system upgrade started")

    def ssh_connect(self, ip, port, uname, passwd):
        self.log.info("upgrading machine <{}>".format(ip))
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(ip, port, uname, passwd)
        if self.ssh:
            self.log.info("ssh connection succeed")
            return True
        else:
            self.log.error("ssh connection failed")
            return False

    def ssh_disconnect(self):
        self.ssh.close()
        self.log.info("ssh connection disconnected")

    def run_script(self, ip):
        self.log.info("running update script")
        cmd = 'sh update_emmc.sh '+ str(ip)
        self._run_command(cmd)

    def terminate(self):
        pass

    def _run_command(self, cmd):
        self.log.info("running: {}".format(cmd))
        _, stdout, stderr = self.ssh.exec_command(cmd)
        data_array_return = stdout.read().decode()
        for line in data_array_return.split("\n"):
            self.log.info(str(line))


def upgrade_func(map):
    upgrade = SystemUpgrade()
    ip = map[0]
    port = map[1]
    uname = map[2]
    passwd = map[3]
    new_ip = map[4]
    
    print("start updating machine #{}".format(ip))
    
    if not upgrade.ssh_connect(ip, port, uname, passwd):
        print("failed connect to the server")
    
    print("runnig emmc upgrade's script")
    if(upgrade.run_script(new_ip)):
        print("failed to run script")
    
    upgrade.ssh_disconnect()
    print("machine upgrade finished\n")
    
    upgrade.terminate()
    print("system upgrade finished\n")


def main():
    thread_list = []
    print("starting system upgrade. log file @upgrade.log")

    for map in maps_list:
        print("creating thread..")
        t = threading.Thread(target=upgrade_func, args=(map,))
        thread_list.append(t)

    for thread in thread_list:
        print("running thread function..")
        thread.start()

    for thread in thread_list:
        print("waiting for thread to finish..")
        thread.join()
        

if __name__ == "__main__":
    main()