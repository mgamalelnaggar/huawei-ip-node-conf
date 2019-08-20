__author__ = 'mgamal'
import paramiko
import time

username = 'eventum'
password = 'P@ssw0rd123'
##########################
infile = "iplist.txt"
command = "commands.txt"
##########################
list = open(infile, 'r')
commands = open (command, 'r')

ip_list = list.readlines()
command_line = commands.readlines()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for node in ip_list:
    client.connect(node.strip('\n'), username=username, password=password, look_for_keys=False, allow_agent=False)
    remote_conn = client.invoke_shell()
    for comm in command_line:
        remote_conn.send(comm)
        time.sleep(1)
        output = remote_conn.recv(65535)
        print output
    remote_conn.close()