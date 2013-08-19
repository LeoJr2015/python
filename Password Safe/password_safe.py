#!/usr/bin/env python
import sqlite3
from Crypto.Cipher import AES
import os
import getpass

def hexdump(src, length=8): 
    result = [] 
    digits = 4 if isinstance(src, unicode) else 2 
    for i in xrange(0, len(src), length): 
       s = src[i:i+length] 
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s]) 
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s]) 
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) ) 
    return b'\n'.join(result)

class AES_Crypto:
	def set_key(self,key):
		pad_to = 16 - (len(key) % 16)
		key = key + ("\x00"*pad_to)
		self.obj = AES.new(key,AES.MODE_ECB)
	def encrypt(self,message):
		pad_to = 16 - (len(message) % 16)
		message = message + ("\x00"*pad_to)
		return self.obj.encrypt(message)
	def decrypt(self,message):
		try:
			decrypted = self.obj.decrypt(message)
			decrypted = decrypted.rstrip('\x00')
			return decrypted
		except:
			return message		

class database:
	def __init__(self,file_name):
		self.c = sqlite3.connect(file_name)
		#self._create()
		self.enc = AES_Crypto()
		
	def _createdb(self):
		self.c.execute("create table if not exists passwords (id INTEGER PRIMARY KEY,description text, username text, password text, category integer)")
 		self.c.execute("create table if not exists unlock (id INTEGER PRIMARY KEY, name text, key blob)")
 	
 	def create_master_key(self):
		result = self.c.execute("select count(*) from unlock where name = 'master'")
		number = result.fetchall()[0][0]
		if number > 0:
			print "Key has already been generated"
		else:
			random = buffer(os.urandom(128))
			self.c.execute("insert into unlock (name,key) values (?,?)" , ("master",random))
		self.c.commit()
		
	def encrypt_master_key(self,key):
		result = self.c.execute("select count(*) from unlock where name = 'encrypt'")
		number = result.fetchall()[0][0]
		if number > 0:
			print "Master Key has already been encrypted"
		else:
			self.enc.set_key(key)
			result = self.c.execute("select (key) from unlock where name = 'master'")
			result = str(result.fetchall()[0][0])
			encryptedkey = self.enc.encrypt(result)
			self.c.execute("insert into unlock (name,key) values (?,?)" , ("encrypt",buffer(encryptedkey)))
			self.c.commit()
			
	def check_for_master_key(self):
		result = self.c.execute("select count(*) from unlock where name = 'encrypt'")
		number = result.fetchall()[0][0]
		if number > 0:
			return True
		else:
			return False
	
	def validate_key(self,key):
		self.enc.set_key(key)
		result = self.c.execute("select (key) from unlock where name = 'master'")
		master = str(result.fetchall()[0][0])
		result = self.c.execute("select (key) from unlock where name = 'encrypt'")
		result = str(result.fetchall()[0][0])
		self.master_key = result
		encrypt = self.enc.decrypt(result)

		#print "Result1= ", hexdump(master)
		#print "Reulst2= ", hexdump(encrypt)
		if encrypt == master:
			#print "valid input"
			return True
		else:
			#print "invalid input"
			return False
		
	def insert(self,fields):
		 ds = fields['description']
		 un = fields['username']
		 pw = fields['password']
		 self.c.execute("insert into passwords (description,username,password) values (?,?,?)" , (ds,un,pw))
		 self.c.commit()
		 
	def get(self,description):
		for row in self.c.execute("select username,password from passwords where description = ?",[description]):
			return (row[0], row[1])
	def get_list(self):
		passwd_list = []
		item = 1
		for row in self.c.execute("select description from passwords"):
			#print row[0]
			passwd_list.append(row[0])
			print item,"-" ,row[0]
			item += 1
		return passwd_list
		
def main():
	entry = {}
	
	db = database('test.db')
	enc = AES_Crypto()
	granted = False
	while (granted == False):
		if (db.check_for_master_key()):
			print "Master Key Exists"
			
			while (granted == False):
				user_key = getpass.getpass("Enter your User Key: ")
				if  (db.validate_key(user_key)):
					print "Access Granted"
					enc.set_key(user_key)
					granted = True
				else:
					print "Access Denied"
		else:
			print "No Master Key"
			match = False
			while (match == False):
				user_key = getpass.getpass("Create User Key: ")
				confirm = getpass.getpass("Confirm your User Key: ")
			
				if user_key == confirm:
					db.create_master_key()
					db.encrypt_master_key(user_key)
					match = True
			
				else:
					print "No Match"
	
	kill = 0
	#db.insert(entry)
	#db.get('Facebook')
	choice = -1
	while (kill==0):
		
		print "*******************"
		print "***Password Safe***"
		print "*******************"
		print "What would you like to do?"
		print "1. Insert item"
		print "2. Fetch item"
		print "3. Quit"
		try:
			choice = int(raw_input("\n>"))
		except: 
			print "Not a Valid Entry"
			quit()
		if choice == 1:
			entry['description'] = raw_input("Description: ")
			entry['username'] = buffer(enc.encrypt(raw_input("Username: ")))
			entry['password'] = buffer(enc.encrypt(raw_input("Password: ")))
			db.insert(entry)

		elif choice == 2:
			passwd_list = db.get_list()
			if (len(passwd_list)):
				pwd_choice = int(raw_input("Which item? "))
				item = db.get(passwd_list[pwd_choice-1])
				for field in item:
					print enc.decrypt(field)
			else:
				print "No Items"
		elif choice == 3:
			kill = 1    
	
	 
if __name__ == '__main__':
	main()

	
	
