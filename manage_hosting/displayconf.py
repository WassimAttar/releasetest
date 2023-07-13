# coding: utf-8

class DisplayConf :

	__createConfTemplate = """
##########################
accès {0}

{1}
{2}
##########################
"""

	__deleteConfTemplate = """
##########################

Compte {1} et Domaine {0} supprimés

##########################
"""

	def __init__ (self,params) :
		self.__params = params

	def create(self,text) :
		if self.__params.get("withwww") :
			domain = "www.{0}".format(self.__params.get("domain"))
			url = "http://{0}".format(domain)
		else :
			if self.__params.get("domain") == "" :
				domain = "http://{0}/{1}".format(self.__params.get("ip"),self.__params.get("account"))
				url = domain
			else :
				domain = self.__params.get("domain")
				url = "http://{0}".format(domain)
		return DisplayConf.__createConfTemplate.format(domain,url,text)

	def delete(self,text) :
		conf = DisplayConf.__deleteConfTemplate.format(self.__params.get("domain"),self.__params.get("account"))
		conf += text
		return conf
