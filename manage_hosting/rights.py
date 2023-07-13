# coding: utf-8

class Rights :

	__rights = "/root/droits.sh"

	def __init__(self,params,Linux) :
		self.__exist = False
		self.__params = params
		self.__Linux = Linux
		self.__rights = Rights.__rights

	def __del__(self):
		if self.__params.get("action") == "create" and not self.__exist :
			self.__Linux.executeShellCommand("sh "+self.__rights)

	def exist(self):
		cmd = "chown -R {0}:{0} {1}".format(self.__params.get("account"),self.__params.get("hostingPath"))
		file = open(Rights.__rights, 'r+')
		content = file.read()
		if content.find(cmd) == -1 :
			return ""
		else :
			self.__exist = True
			return "Rights {0} already exists\n".format(self.__params.get('account'))

	def create(self):
		cmd = "chown -R {0}:{0} {1}".format(self.__params.get('account'),self.__params.get("hostingPath"))
		if self.__params.get("verbose") :
			print(cmd)
		if self.__params.get("execute") :
			file = open(Rights.__rights, 'r+')
			content = file.read()
			file.seek(0, 0)
			file.write(cmd+"\n"+content)
			file.close()
		return ""

	def delete(self):
		text = "chown -R {0}:{0}".format(self.__params.get('account'))
		self.__Linux.executeShellCommand("sed -i '/{0}/d' {1}".format(text,Rights.__rights))
		return ""