import thread
import socket
import sys
import select
import json

sms_buffer = 500000000

leftMembers = {}


def chat(appSocket):
	while 1:
		selectList = [sys.stdin, appSocket]
		(read,write,err) = select.select(selectList,[],[],0)
		for ss in read:
			if ss == appSocket:
				msg = ss.recv(sms_buffer)
				print msg
			else:
				#print "-------------------------------"
				msg = raw_input("[::]")
				#print "-------------------------------"
				appSocket.send(msg)


def file(appSocket):
	print "entered in file client"
	while 1:
		selectList = [sys.stdin, appSocket]
		(read,write,err) = select.select(selectList,[],[],0)
		for ss in read:
			if ss == appSocket:
				print "going to recv"
				ff = ss.recv(1024)
				with open('clientReceived','wb') as fd:
					while ff:
						
						print(". . .")
						fd.write(ff)
						ff = ss.recv(1024)
						

				fd.close()
				#print "Downloaded"


				
			else:
				print "going to snd"
				fn = raw_input("")
				fd = open(fn,'rb')
				fh = fd.read(1024)
				while fh:
					appSocket.send(fh)
					print ". . ."
					fh = fd.read(1024)
				fd.close()
				print "Sending Complete"
				#appSocket.send("Hello")
				
######################## two tasks tiill DONE ##################################################


def bar(appSocket,name):
	print 'getting your groups'
	appSocket.send(name)
	#ok1 = appSocket.recv(1024)
	i= 1
	#si1 = appSocket.recv(1024)
	#appSocket.send("ok") # qwe
	#si = int(si1)
	ai = 1
	li = []
	#while ai <= si:
	fms = appSocket.recv(1024)
	li = json.loads(fms)
	#li.append(fms)
	#ai =ai+1



	for k in li:
		print "%s - %s  \n" %(i,k) 
		i = i+1
	print "M - Make a group"
	acG = "to be filled"
	ind = raw_input("Enter your option: ")
	if ind != "M":
		ind3 = (int(ind)-1)
		if(len(li)>0):
			acG = li[ind3]
			return (ind,acG)
	else:
		return (ind," ")

def group(appSocket,name):
	ind,acG = bar(appSocket,name)
	nameGroup = " "
	if(ind == "M"):
		appSocket.send("M")
		print"Enter Names to add in group, Enter :q when all OK with names"
		abc = "a"
		memList2 = []
		while abc != ":q":
			mem = raw_input ("name of member: ")
			if mem != ":q":
				memList2.append(mem)
			abc = mem
		n = raw_input("Name of Group:")
		nameGroup = n
		memList2.append(name)
		groupList.append(n)
		memList2.append(n)
		
		# sending size of list to server
		lth = "%d" %(len (memList2))
		print lth
		appSocket.send(lth)
		#sending names of member
		ok = appSocket.recv(1024)
		print ok
		for l in memList2:
			appSocket.send(l)
			ok = appSocket.recv(1024)
			print ok
		#appSocket.send(n)
		
		memList.append(memList2)
		print "DONE \n"
		ms = appSocket.recv(1024)
		print ms
		print "\n"
		group(appSocket,name)

	if ind != "M":
		print "1- Members"
		print "2 - Chat"
		print "3 - Leave group"
		print "4 - Add Member"
		print "5 - Broadcast file"
		ind2 = raw_input("select: ")
		appSocket.send("not_M")
		appSocket.recv(1024) # 112
		if ind2 == "4":
			# iWn = ["4",name]
			# iWn = json.dumps(iWn)
			appSocket.send("4")


			faltuaswell = appSocket.recv(1024)
			appSocket.send(acG)

			
			faltu = appSocket.recv(1024)
			appSocket.send(name)


			res = appSocket.recv(1024)

			res = json.loads(res)
			if(res[0] == "You are not admin"):
				print res[0]
				print "Admin is %s" %res[1]
			else:
				mem2add = raw_input('name: ')
				appSocket.send(mem2add)
				

		if ind2 == "2":
			appSocket.send("2")
			msggg = appSocket.recv(1024)
			if msggg == 'tellName':
				appSocket.send(nameGroup)
			chat(appSocket)
		if ind2 == "3":
			appSocket.send("3")
			appSocket.send(acG)
			print "please confirm your name for security issues"
			nam = raw_input("YOUR NAME: ")
			appSocket.send(nam);
		if ind2 == "1":
			appSocket.send("1")
			#acG is the name of active group
			appSocket.send(acG) # 120A
			siAA = appSocket.recv(1024)
			siA = int(siAA)
			aa =1
			#memA will receive members of group from server
			memA = []
			while aa <= siA:
				sss = appSocket.recv(1024)
				memA.append(sss)
				appSocket.send("ok")
				aa = aa+1

			dic = appSocket.recv(1024)
			leftMembers = json.loads(dic)
			if(acG in leftMembers):
				allLeft = (leftMembers[acG])
			else:
				allLeft = []
			#print allLeft
			# print leftMembers
			# print 'yahi tha'

			mem2show = []
			for ele in memA:
				elemen = ele.split(" ")
				#print elemen
				if(not(elemen[0] in allLeft)):
					 ss = "-- " + ele
					 mem2show.append(ss)

			ss = mem2show[len(mem2show)-2]
			ss = ss+ "     info:ADMIN"
			mem2show[len(mem2show)-2] = ss

			for a in mem2show:
				print a


			ss = ss.split(" ")
			if(name == ss[1]):
				yesOrNo = raw_input('want to change admin? (y/n)')
				if(yesOrNo == "y"):
					newAdmin = raw_input('New Admin Name (choose one from above shown members)')
					newAdmin = [name,newAdmin]
					newAdmin = json.dumps(newAdmin)
					appSocket.send(newAdmin)

				else:
					ok = ["ok"]
					ok = json.dumps(ok)
					appSocket.send(ok)

			else:
				ok = ["ok"]
				ok = json.dumps(ok)
				appSocket.send(ok)

		#	print leftMembers
			# try:
			# 	allLeft = (leftMembers[acG])
			# 	for l in allLeft:
			# 		print l
			# except:
			# 	pass
		#main()
		#group(appSocket,name)
		if(ind2 == "5"):
			appSocket.send("5")

			file(appSocket)






activeGroup = []
memList = []
groupList = []
def main():
	IP = "127.0.0.1"
	PORT = input("PORT: ")

	appSocket = socket.socket()
	appSocket.connect((IP,PORT))
	print "CONNECTED TO SERVER "
	n = raw_input("NAME: ")
	name = n
	appSocket.send(n)
	s = raw_input("status: ")
	appSocket.send(s)

	
	# print "1- Chat a friend"
	# print "2- Files"
	# print "3- Groups"
	menu = appSocket.recv(sms_buffer)
	menu = json.loads(menu)
	for m in menu:
		print m
	# try:
	# 	menu = appSocket.recv(sms_buffer)
	# 	print menu
	# except:
	# 	pass
	
	option = raw_input("ENTER : ")

	appSocket.send(option)

	
	if option == "1":
		chat(appSocket)
	if option == "2":
		file(appSocket)
	if option == "3":
		group(appSocket,name)
	if option == "4":
		offmsgs = appSocket.recv(1024)
		offmsgs = json.loads(offmsgs)
		for m in offmsgs:
			print m
	while(1):
		continue


if __name__ == "__main__":
	main()
