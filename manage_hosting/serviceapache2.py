# coding: utf-8

import os

class Apache2() :

	__apacheConfPath = "/etc/apache2/sites-available/"

	__apacheTemplate = """
<VirtualHost  *:80>
    ServerAdmin 132049@free.fr
    DocumentRoot {0}
    ServerName {2}
    ErrorLog /var/log/apache2/{1}_error.log
    CustomLog /var/log/apache2/{1}_access.log combined
    {3}

    AssignUserId {1} {1}
    php_admin_value open_basedir "{4}/:/tmp/"

   <Directory {0}>
     Options -Indexes
     AllowOverride All
     Require all granted
    </Directory>

  <DirectoryMatch "{0}/(cache|upload)/">
    php_flag engine off
  </DirectoryMatch>

</VirtualHost>
"""

	__apacheTemplateNoDomain = """
<Directory {0}>
  AssignUserId {1} {1}
  php_admin_value open_basedir "{2}/:/tmp/"

  Options -Indexes
  AllowOverride All
  Require all granted
</Directory>

<DirectoryMatch "{0}/(cache|upload)/">
  php_flag engine off
</DirectoryMatch>
"""

	def __init__(self,params,Linux):
		self.__exist = False
		self.__params = params
		self.__Linux = Linux
		if self.__params.get("domain") == "" :
			self.__confFile = self.__params.get("account")
		else :
			self.__confFile = self.__params.get("domain")
		self.__apacheConfFile = "{0}{1}.conf".format(Apache2.__apacheConfPath,self.__confFile)

	def __del__(self):
		if self.__params.get("action") != "" and self.__params.get("execute") and not self.__exist :
			self.__reloadApache()

	def __enableVhostApache(self) :
		self.__Linux.executeShellCommand("a2ensite "+self.__confFile+".conf")

	def __disableVhostApache(self) :
		self.__Linux.executeShellCommand("a2dissite "+self.__confFile+".conf")

	def __reloadApache(self) :
		self.__Linux.executeShellCommand("systemctl reload apache2")

	def exist(self):
		if os.path.exists(self.__apacheConfFile) :
			self.__exist = True
			return "Apache conf file {0} already exists\n".format(self.__apacheConfFile)
		else :
			return ""

	def create(self) :
		if self.__params.get("withwww") :
			serverAlias = "ServerAlias www.{0}".format(self.__params.get("domain"))
		else :
			serverAlias = ""
		documentRootVhost = self.__params.get("hostingPathVhost")+self.__params.get("documentRootVhost")
		openBaseDir = self.__params.get("hostingPath")
		if not os.path.isdir(documentRootVhost) :
			self.__Linux.executeShellCommand("mkdir {0}".format(documentRootVhost))
		if self.__params.get("domain") == "" :
			apacheConf = Apache2.__apacheTemplateNoDomain.format(documentRootVhost,self.__params.get("account"),openBaseDir)
		else :
			apacheConf = Apache2.__apacheTemplate.format(documentRootVhost,self.__params.get("account"),self.__params.get("domain"),serverAlias,openBaseDir)
		if self.__params.get("verbose") :
			print(apacheConf)
		if self.__params.get("execute") :
			file = open(self.__apacheConfFile, 'w')
			file.write(apacheConf)
			file.close()
		self.__enableVhostApache()
		return ""

	def delete(self) :
		self.__disableVhostApache()
		self.__Linux.executeShellCommand("rm {0}".format(self.__apacheConfFile))
		return ""