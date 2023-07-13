# coding: utf-8

import re

try:
	import MySQLdb
except ImportError:
	print("Please install MySQLdb")
	exit()

class Mysql() :

	__mysqlConfFile = "/root/.my.cnf"

	__createConfTemplate = """
Base de données :
http://{0}/phpmyadmin/
login : {1}
pass : {2}
"""

	def __init__ (self,params,Linux) :
		self.__params = params
		self.__Linux = Linux
		self.__createMysqlInstance()

	def __del__(self):
		try :
			self.mysqlInstance.close()
		except :
			pass

	def __createMysqlInstance(self) :
		mysqlRootPassword = self.__getMysqlRootPassword()
		self.mysqlInstance = MySQLdb.connect(host="localhost",user="root",password=mysqlRootPassword)

	def __getMysqlRootPassword(self) :
		try :
			file = open(Mysql.__mysqlConfFile, 'r')
		except IOError :
			print("Please create {}".format(Mysql.__mysqlConfFile))
			exit()
		content = file.read()
		file.close()
		try :
			return(re.findall('password=(.*)', content)[0])
		except IndexError :
			print("""Please enter mysql root password in {0} file.
Example :
[client]
password=p4ssw0rD
Protect this file
chmod 600 {0}""".format(Mysql.__mysqlConfFile))
			exit()

	def executeSqlRequest(self,cursor,request) :
		cursor.execute(request)
		result=cursor.fetchone()
		if result != None :
			return True
		else :
			return False

	def __mysqlUserExists(self) :
		cursor = self.mysqlInstance.cursor()
		return self.executeSqlRequest(cursor,"select User from mysql.user where User = '{0}'".format(self.__params.get("account")))


	def exist(self):
		if self.__mysqlUserExists() :
			return "mysql user {0} already exists\n".format(self.__params.get("account"))
		return ""

	def create(self) :
		mysqlPassword = self.__Linux.generateRandomString(12)
		queries = ("CREATE USER '{0}'@'localhost' IDENTIFIED BY '{1}'",
                    "GRANT USAGE ON * . * TO '{0}'@'localhost' IDENTIFIED BY '{1}' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0",
                    "CREATE DATABASE IF NOT EXISTS `{0}`",
                    "GRANT ALL PRIVILEGES ON `{0}` . * TO '{0}'@'localhost'")
		for query in queries :
			query = query.format(self.__params.get("account"),mysqlPassword)
			if self.__params.get("verbose") :
				print(query)
			if self.__params.get("execute") :
				cursor = self.mysqlInstance.cursor()
				cursor.execute(query)
			return Mysql.__createConfTemplate.format(self.__params.get('ip'),self.__params.get('account'),mysqlPassword)

	def delete(self) :
		queries = ("DROP USER '{0}'@'localhost'",
                           "DROP DATABASE IF EXISTS `{0}`"
			)
		for query in queries :
			query = query.format(self.__params.get("account"))
			if self.__params.get("verbose") :
				print(query)
			if self.__params.get("execute") :
				try :
					cursor = self.mysqlInstance.cursor()
					cursor.execute(query)
				except :
					print("Base déjà supprimée")
			return ""
