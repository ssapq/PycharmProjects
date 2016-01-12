__author__ = 'ss'
#!/usr/bin/python
#filename easyhadoop1.py
import os
import sys
import subprocess
import pexpect
import getpass
import shutil

java_source="jdk1.7.0"
java_dest="/usr/java/"

def buildSSH(username,psw):
	try:
		serverlist = open('server.txt','r')
		for server in serverlist:
			child=pexpect.spawn("ssh %s -l %s 'ssh-keygen -t rsa'"%(server.split('\t')[1].rstrip(),username))
			index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==1:
				child.sendline('yes')
				index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==2:
				child.sendline(psw)
	     			ret=child.expect([pexpect.TIMEOUT,'Enter file in which to save the key.* '])
	     			if ret==1:
	             			child.sendline()
	             			ret=child.expect([pexpect.TIMEOUT,'Overwrite.*','Enter passphrase.* '])
					if ret==1:
						child.sendline('y')
	             				ret=child.expect([pexpect.TIMEOUT,'Overwrite.*','Enter passphrase.* '])
	             			if ret==2:
	                     			child.sendline()
	                     			ret=child.expect([pexpect.TIMEOUT,'Enter same passphrase again: '])
	                     			if ret==1:
	                             			child.sendline()
	                             			child.expect(pexpect.EOF)
	finally:
		serverlist.close()

def copyPub2Auth(username,psw):
	try:
		serverlist=open('server.txt','r')
		for server in serverlist:
			# build authorized_keys
			child=pexpect.spawn("ssh %s -l zhoulei 'cp .ssh/id_rsa.pub .ssh/authorized_keys'"%server.split('\t')[1])
			index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==1:
				child.sendline('yes')
				index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==2:
				child.sendline(psw)
				child.expect(pexpect.EOF)
			# change file mode
			child=pexpect.spawn("ssh %s -l %s 'chmod 600 .ssh/authorized_keys'"%(server.split('\t')[1],username))
			index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
	        	if index==1:
	                	child.sendline('yes')
	                	index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
	        	if index==2:
	                	child.sendline(psw)
	                	child.expect(pexpect.EOF)
			# cat file content to authorized_keys
			auth=open('../.ssh/authorized_keys','a+')
			child=pexpect.spawn("ssh %s -l %s 'cat .ssh/authorized_keys'"%(server.split('\t')[1],username))
			index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==1:
				child.sendline('yes')
                                index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==2:
				child.sendline(psw)
				child.expect(pexpect.EOF)
				content=child.before
				auth.write(content.rstrip())
			auth.close()

	finally:
		serverlist.close()
		auth.close()

def copyAuth2Server(username,psw):
	try:
		serverlist=open('server.txt','r')
		for server in serverlist:
			print "scp ../.ssh/authorized_keys %s@%s:~/.ssh/"%(username,server.split('\t')[1].rstrip())
			child=pexpect.spawn("scp ../.ssh/authorized_keys %s@%s:~/.ssh/"%(username,server.split('\t')[1].rstrip()))
			index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==1:
				child.sendline('yes')
				index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==2:
				child.sendline(psw)
				child.expect(pexpect.EOF)
	finally:
		serverlist.close()

def buildKnowList():
	try:
		ex=os.path.exists(r'../.ssh/known_hosts')
		if ex==True:
			os.remove(r'../.ssh/known_hosts')
                serverlist=open('server.txt','r')
		namenode=""
		i=0
                for server in serverlist:
			if i==0:
				namenode=server.split('\t')[1].rstrip()
			print "ssh %s -l zhoulei -tt 'ssh %s'"%(namenode,server.split('\t')[1].rstrip())
                        child=pexpect.spawn("ssh %s -l zhoulei -tt 'ssh %s'"%(namenode,server.split('\t')[1].rstrip()))
                        index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==2:
                                child.sendline(psw)
                                index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
                        if index==1:
                                child.sendline('yes')
			i+=1
	finally:
                serverlist.close()

def copyKnowList():
	try:
		serverlist=open('server.txt','r')
		namenode=""
		i=0
		for server in serverlist:
			if i==0:
				namenode=server
			print "scp ../.ssh/known_hosts %s@%s:~/.ssh/"%(username,server.split('\t')[1].rstrip())
			child=pexpect.spawn("scp ../.ssh/known_hosts %s@%s:~/.ssh/"%(username,server.split('\t')[1].rstrip()))
			index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==1:
				child.sendline('yes')
				index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==2:
				child.sendline(psw)
				child.expect(pexpect.EOF)
		i+=1
	finally:
		serverlist.close()

def disableIpTable(rootpsw):
	try:
		serverlist=open('server.txt','r')
		for server in serverlist:
			child=pexpect.spawn("ssh %s 'service iptables stop'"%server.split('\t')[1].rstrip())
			index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==1:
				child.sendline('yes')
				index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
			if index==2:
				child.sendline(rootpsw)
				child.expect(pexpect.EOF)
			child=pexpect.spawn("ssh %s 'chkconfig --del iptables'"%server.split('\t')[1].rstrip())
                        index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
                        if index==1:
                                child.sendline('yes')
                                index=child.expect([pexpect.TIMEOUT,'Are you sure you want to continue connecting.*','password:'])
                        if index==2:
                                child.sendline(rootpsw)
                                child.expect(pexpect.EOF)
			if index==0:
				print 'timeout please check you root password'
				sys.exit(0)
	finally:
		serverlist.close()

#def modifyUlimit():


def buildEnvironment():
	if os.path.exists(java_source)==False:
		print "can't find java_source"
		return False;
	if os.path.exists(java_dest)==False:#path is not exists
		ret=subprocess.call("mkdir %s"%java_dest,shell=True)
		if ret==0:
			ret=subprocess.call("cp -r %s %s"%(java_source,java_dest),shell=True)
		return True
	elif os.path.exists(java_dest+java_source)==True:#path is exists
		return True
	else:# other
		ret=subprocess.call("cp -r %s %s"%(java_source,java_dest),shell=True)
		return True

def copyBySSH(fr,to,psw):
	if os.path.exists(fr)==False:
		print "Can't find from path"
	else:
		print "scp -r %s %s"%(fr,to)
		child = pexpect.spawn("scp -r %s %s"%(fr,to))
		index=child.expect([pexpect.TIMEOUT,"password: "])
		#print index
		if index==1:
			#print psw
			child.sendline(psw)
			#child.expect(pexpect.EOF)
		else:
			return False

def echoProfile():
	print "echo 'JAVA_HOME=%s'>>/etc/profile"%(java_dest+java_source)
	ret = subprocess.call("echo 'JAVA_HOME=%s'>>/etc/profile"%(java_dest+java_source),shell=True)
	print "echo 'PATH=$JAVA_HOME/bin:$PATH'>>/etc/profile"
	ret = subprocess.call("echo 'PATH=$JAVA_HOME/bin:$PATH'>>/etc/profile")
	if ret == 0:
		ret = subprocess.call("ssh server -l source /etc/profile'",shell=True)
		return True
	else:
		return False

if __name__=="__main__":
	#sys.argv.length
	username=raw_input('login username: ')
	psw=getpass.getpass("login password: ")
	i=0
	while username=='' or psw=='':
		print "Usage: must input you login username and password"
		username=raw_input('login username: ')
        	psw=getpass.getpass("login password: ")
		i+=1
		if i>=2:
			print "Usage: error!,system.exit(0),must have username and password"
			sys.exit(0)
	rootpsw=getpass.getpass('root password:')
	while rootpsw=='':
		print "Usage: must input you root password"
        	rootpsw=getpass.getpass("root password: ")
		i+=1
		if i>=2:
			print "Usage: error!,system.exit(0),must have root password"
			sys.exit(0)

	buildSSH(username,psw)
	copyPub2Auth(username,psw)
	copyAuth2Server(username,psw)
	buildKnowList()
	copyKnowList()
	disableIpTable(rootpsw)
	#modifyUlimit()
	#copyJDk()
	ret = buildEnvironment()
	if ret==False:
		sys.exit(0)
	fr=java_dest+java_source
	try:
		serverlist = open("server.txt",'r')
		for server in serverlist:
			to=server.split('\t')[1].rstrip()+":"+java_dest
			copyBySSH(fr,to,rootpsw)
		#ret = echoProfile()
		#for server in serverlist:
		#	print "server:"+server
		#	fr="/etc/profile"
		#	to=server.split('\t')[1].rstrip()+":"+"/etc/"
		#	copyBySSH(fr,to)
		#for server in serverlist:
		#	echoHosts(server)
	finally:
		serverlist.close()
