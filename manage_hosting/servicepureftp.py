# coding: utf-8

class Pureftp() :

	__hostingPath = "/var/www/"
	__pureftpDatabase = "pureftpd"

	__createConfTemplate = """
ftp :
ip : {0}
login : {1}
pass : {2}
protocol : ftp
"""

	def __init__(self,params,Mysql,Linux) :
		self.__params = params
		self.__Linux = Linux
		self.__Mysql = Mysql
		try :
			self.__Mysql.mysqlInstance.select_db(Pureftp.__pureftpDatabase)
		except	:
			print("Unknown database 'pureftpd'")
			exit()
		self.__cursor = self.__Mysql.mysqlInstance.cursor()

	def __pureftpHostingPathExists(self) :
		return self.__Mysql.executeSqlRequest(self.__cursor,"select Dir from users where Dir = '{0}'".format(self.__params.get("hostingPath")))

	def __pureftpUserExists(self) :
		return self.__Mysql.executeSqlRequest(self.__cursor,"select User from users where User = '{0}'".format(self.__params.get("account")))

	@staticmethod
	def getHostingPath(account) :
		return "{0}{1}".format(Pureftp.__hostingPath,account)

	def exist(self):
		display = ""
		if self.__pureftpHostingPathExists() :
			display +=  "ftp hosting path {0} already exists\n".format(self.__params.get("hostingPath"))
		if self.__pureftpUserExists() :
			display +=  "ftp user {0} already exists\n".format(self.__params.get("account"))
		return display

	def create(self) :
		self.__Linux.createUser("/bin/false","")
		self.__Linux.executeShellCommand("rm {0}/.bash_logout {0}/.bashrc {0}/.profile".format(self.__params.get("hostingPath")))
		try:
			pureftpPassword = self.__Linux.generateRandomString(12)
			uid = self.__Linux.getUid()
			query = """INSERT INTO `users` ( `User` , `Password` , `Uid` , `Gid` , `Dir` )
									VALUES ('{0}', MD5('{1}') , '{2}', '{2}', '{3}');""".format(self.__params.get("account"),pureftpPassword,uid,self.__params.get("hostingPath"))
			if self.__params.get("verbose") :
				print(query)
			if self.__params.get("execute") :
				self.__cursor.execute(query)
		except KeyError:
			if self.__params.get("verbose") :
				print('Linux user {0} not created, can\'t create ftp user {0} yet\n'.format(self.__params.get("account")))
		return Pureftp.__createConfTemplate.format(self.__params.get('ip'),self.__params.get('account'),pureftpPassword)

	def delete(self) :
		query = """DELETE FROM `users` WHERE `User`= '{0}' and `Dir`='{1}';
						""".format(self.__params.get("account"),Pureftp.getHostingPath(self.__params.get("account")))
		if self.__params.get("verbose") :
			print(query)
		if self.__params.get("execute") :
			self.__cursor.execute(query)
		return ""