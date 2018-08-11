import socket
import thread
import sys
import select
import json

sms_buffer = 50000000
#contains all connected [sock,name]
socketsList = []

# contains all connected sockets
realList = []

#last is acG
memList2 = []

leftMem = {} # group name to [left members]

offSMS = {} # messages of thos who are


statusList = {}
def acceptClients(serSocket):
	print "accepting"
	while True:
		sock,addr = serSocket.accept()
		name = sock.recv(sms_buffer)
		socketsList.append([sock,name])
		status = sock.recv(sms_buffer)
		statusList[name] = status
		realList.append(sock)
		print "%s is connected" %name
		thread.start_new_thread(clients,(sock,serSocket,name))
		

activeGroup = []
memList = []
groupList = []
def main():
	IP = "127.0.0.1"
	PORT = input("Port: ")
	serSocket = socket.socket();
	serSocket.bind((IP,PORT))
	print "Server Ready"

	serSocket.listen(5)
	socketsList.append([serSocket,"SERVER"])
	realList.append(serSocket)
	acceptClients(serSocket)
	





def clients(sock,ser,name):
	
	# sock.send("1 - CHAT A FRIEND ")
	# sock.send("2 - FILES ")
	# sock.send("3 - GROUPS \n")
	menuToSend = ["1 - CHAT A FRIEND \n","2 - FILES \n","3 - GROUPS \n", "4 - Offline messages"]
	menuToSend = json.dumps(menuToSend)
	sock.send(menuToSend)
	index = sock.recv(sms_buffer)
	print index
	if index == "1":
		print "Directing to Chat ROOM"
		chatFriend(sock,ser)
	if index == "2":
		print "Directing to File Mode"
		fileHandling(sock,ser)
	if index == "3":
		"Directing to Group Mode"
		groupChat(sock,ser)
	if index == "4":
		print 'I am here'
		if name in offSMS:
			offmsgs = offSMS[name]
			# print offSMS
			# print 'already'
			offmsgs = json.dumps(offmsgs)
			sock.send(offmsgs)
		else:
			print offSMS

###############################################################################################################################
def groupChat(sock,ser):
	groupName2 = " " # real as without 2 is already i =n
	memNamesOfACG = [] # construted below contains names of mem of active group
	nn = sock.recv(1024)
	#sock.send("ok")
	nnList = []
	nnListwM = []
	for op in memList:
		for p in op:
			if p == nn:
				nnList.append(op[(len (op))-1])
				nnListwM.append(op)
	print "SO:"
	for a in nnList:
		print a
	print "its all"
	si1 = len(nnList)
	si = "%d" %si1 
	if(len(nnListwM) > 0):
		groupName2 = nnListwM[len(nnListwM)-1]
	#sock.send(si)
#	ok = sock.recv(1024) # qwe
	# for a in nnList:
	# 	sock.send(a)

	groupList2Send = json.dumps(nnList)
	sock.send(groupList2Send)


	#receiving "M" or anything
	opt = sock.recv(1024)
	if opt == "M":
		lth1 = sock.recv(1024)
		print lth1
		sock.send("ok")
		lth = int(lth1)
		
		i = 0
		while (i < lth):
			mem = sock.recv(1024)
			sock.send("ok")
			print "adding %s" %mem
			memList2.append(mem)

			i = i+1

		groupName = memList2[(len (memList2))-1]
		groupList.append(groupName)
		#memList2.append(groupName)
		memList.append(memList2)
		jsms = "GROUP %s created with %s members" %(groupName,lth-1)
		sock.send(jsms) 
		groupChat(sock,ser)
		#################DONE MAKING##################
	if opt != "M":
		sock.send("ok") #112
		p2 = sock.recv(1024)
		if p2 == "2":
			sock.send('tellName')
			acG = sock.recv(1024)
			thread.start_new_thread(chatFriendG,(sock,ser, acG))

		if p2 == "3":
			#leave group req
			acG = sock.recv(1024)
			print("%s shrinking a member") %acG
			nam = sock.recv(1024)
			print ("%s leaving") %nam

			if(acG in leftMem):
				leftMem[acG] = (leftMem[acG]).append(nam)
			else:
				leftMem[acG] = [nam]

		if p2 == "4":
			sock.send("faltuaswell")
			acG = sock.recv(1024)
			if(acG != " "):
				sock.send("1024") # faltu
				rAD = " " # real amin
				#iWn = json.loads(iWn)
				itsName = sock.recv(1024)
				for pp in nnListwM:
					if(pp[(len(pp))-1]) == acG:
						rAD = pp[len(pp)-2]
				if(itsName == rAD):
					mem2add = ['name','name']
					mem2add = json.dumps(mem2add)
					sock.send(mem2add)
					mem2add = sock.recv(1024)
					for pp in nnListwM:
						if(pp[(len(pp))-1]) == acG:
							# now pp is good to go
							adminInd = len(pp)-2
							pp.append(mem2add)
							gn = pp[len(pp)-1]
							pp[len(pp)-1] = pp[len(pp)-2] # group name on last
							
							pp[len(pp)-2] = pp[len(pp)-3]
							pp[len(pp)-3] = gn

					print nnListwM



				else:
					realAdmin = " "
					for pp in nnListwM:
						if(pp[(len(pp))-1]) == acG:
							# now pp is good to go
							realAdmin = pp[len(pp)-2]

					#realAdmin = nnListwM[(len(nnListwM))-2]
					info4 = ['You are not admin',realAdmin]
					info4 = json.dumps(info4)
					sock.send(info4)

		if p2 == "1":
			acG = sock.recv(1024) # 120A
			activeGroup.append(acG)
			# acNames = activeList(nnListwM,ser)
			# for p in acNames:
			# 	print p
			# 	print "z"
			for pp in nnListwM:
				if(pp[(len(pp))-1]) == acG:
					siA = len(pp)
					siAA = "%d" %siA
					sock.send(siAA)
					inf = " "
					for ele in pp:
						try:
							ele = ele+ "   ->status :: "+ statusList[ele] + " "+ inf
						except:
							pass
						sock.send(ele)
						memNamesOfACG.append(ele)
						ok = sock.recv(1024)

			leftJSON = json.dumps(leftMem)
			sock.send(leftJSON)

			newAdmin = sock.recv(1024)
			newAdmin = json.loads(newAdmin)
			if(newAdmin[0] != "ok"):
				for pp in nnListwM:
					if(pp[(len(pp))-1]) == acG:
						aa,bb = pp.index(newAdmin[1]) , pp.index(newAdmin[0])
						pp[aa],pp[bb] = pp[bb], pp[aa]
		if(p2 == "5"):
			fileHandling(sock,ser)







					
			


###########################################################################################################

def fileHandling(sock,ser):
	while 1:
		file_recv(sock,ser)

def file_recv(sock,ser):
	(read,write,err) = select.select(realList,[],[],0)
	for k in read:
		if (k != ser):
			ff = k.recv(1024)
			with open('serverReceived','wb') as fd:
				while ff:
					print ". . ."
					fd.write(ff)
					print "written"
					print ff
					ff = k.recv(1024)
					#ff = k.recv(sms_buffer)
				print "DOWNLOADED"
				fd.close()
				i=0
				file_send(k,'serverReceived')


def file_send(k,n):
	print "sending trial"
	for sockk in realList:
		if(sockk != k):
			try:
				#print "ander to aa rha hu"
				fh = fd.read(1024)
				fd = open('serverReceived','rb')
				while fh:
					sockk.send(fh)
					print "sending ..."
					fh = fd.read(1024)
				fd.close()
				print "SENT"
				
			except:
				continue


def giveSockgetName(sock):
	for p in socketsList:
		if(p[0] == sock):
			return p[1]

def chatFriendG(sock,ser,acG):
	print memList2
	while 1:
		sms_recvG(sock,ser,acG)

def sms_recvG(sock,ser,acG):
	#print "IN"
	(read,write,err) = select.select(realList,[],[],0)
	for k in read:
		if (k != ser):
			msg = k.recv(sms_buffer)
			print msg
			if msg:
				sendTo2G(k,msg,acG)
			else:
				sendTo2G(k,"GONE DISCONNECTED", acG)
				for n in socketsList:
					if(n[0] == k):
						print "Disconnected : %s"  %n[1]
						offSMS[n[1]] = []
				print offSMS
				realList.remove(k)

def sendTo2G(sender, msgg, acG):
	for socks in realList:
		if(socks != sender):
			try:
				for n in socketsList:
					if(n[0] == sender):
						for_sms = "%s >> %s" %(n[1],msgg)
						socks.send(for_sms)
						for p in offSMS:
							if(msgg != "GONE DISCONNECTED" and (not(for_sms in offSMS[p]))):
								d = offSMS[p] 
								print p
								print offSMS[p]
								iii = "      from Grroup: %s"%acG
								d.append(for_sms + iii)
								offSMS[p] = d
								print offSMS
						

			except:
				continue

def chatFriend(sock,ser):
	while 1:
		sms_recv(sock,ser)

def sms_recv(sock,ser):
	(read,write,err) = select.select(realList,[],[],0)
	for k in read:
		if (k != ser):
			msg = k.recv(sms_buffer)
			print msg
			if msg:
				sendTo2(k,msg)
			else:
				sendTo2(k,"GONE DISCONNECTED")
				for n in socketsList:
					if(n[0] == k):
						print "Disconnected : %s"  %n[1]
						offSMS[n[1]] = []
				print offSMS
				realList.remove(k)

def sendTo2(sender, msgg):
	for socks in realList:
		if(socks != sender):
			try:
				for n in socketsList:
					if(n[0] == sender):
						for_sms = "%s >> %s" %(n[1],msgg)
						socks.send(for_sms)
						print offSMS
						for p in offSMS:
							if(msgg != "GONE DISCONNECTED" and (not(for_sms in offSMS[p]))):
								d = offSMS[p] 
								print p
								print offSMS[p]
								d.append(for_sms)
								offSMS[p] = d
								print offSMS
							else:
								print "A meesgae sent to %s"%socks
						

			except:
				continue

if __name__ == "__main__":
	main()

# select ko jo realList de rha hun, wo change krney se kaam ho jaey ga
	
