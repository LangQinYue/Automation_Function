# -.- coding:utf-8 -.-
__author__ = 'Administrator'

import paramiko


ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect("172.16.200.62", 22, "root", "123456")

stdin, stdout, stderr = ssh.exec_command("ifconfig")

result_msg = stdout.read()


print result_msg


ssh.close()

