# ManageHosting

Command-line program to create web hosting : ssh, ftp, mysql etc... accounts and apache virtualhosts

- [DESCRIPTION](#description)
- [OPTIONS](#options)
- [USE CASES](#use-cases)

### DESCRIPTION
**managehosting** is a commande-line program to easly create web hosting for applications.
Works with python 3.

To run, below services must be installed on a linux box
 - apache
 - mysql
 - pureftp
 - phpmyadmin

Each service has its own class so it can be extensible.
classes for nginx, proftpd, postgres, etc... are easy to create.

### OPTIONS

    --account				The account name of the hosting.
    --domain				The domain name of the hosting.
    --withwww				Adds www. to the domain name.
    --withsql				Creates the Mysql account.
    --withftp				Creates the Pureftp account.
    --withssh				Creates the ssh/sftp account.
    --create				Create accounts.
    --delete				Delete accounts.
    --execute				Execute command. If not used, it's a dry run.
    -v						Verbose mode. All details about the accounts creation.
    -V						Version.
    -U						Update to latest release.

### USE CASES
Create hosting for the domain www.johndoe.com with ftp and mysql accounts

    ./managehosting --account johndoe --domain johndoe.com --withwww --withsql --withftp --create --execute

Output

		##########################
		http://www.johndoe.com

		ftp :
		ip : xxx.xxx.xxx.xxx
		login : johndoe
		pass : Jf29ufOYALAL

		Database :
		http://xxx.xxx.xxx.xxx/phpmyadmin/
		login : johndoe
		pass : dD1M1TXEWGKX
		##########################


Create hosting for the domain www.johndoe.com with ssh/sftp and mysql accounts

    ./managehosting --account johndoe --domain johndoe.com --withwww --withsql --withssh --create --execute

Output

		##########################
		http://www.johndoe.com

		ssh :
		ip : xxx.xxx.xxx.xxx
		login : johndoe
		pass : Jf29ufOYALAL

		Database :
		http://xxx.xxx.xxx.xxx/phpmyadmin/
		login : johndoe
		pass : dD1M1TXEWGKX
		##########################

Create hosting for a static application for the domain johndoe.com with only ftp account

    ./managehosting --account johndoe --domain johndoe.com --withftp --create --execute

Output

		##########################
		http://johndoe.com

		ftp :
		ip : xxx.xxx.xxx.xxx
		login : johndoe
		pass : Jf29ufOYALAL
		##########################

Create hosting without domain name but with ssh/sftp and mysql accounts

    ./managehosting --account johndoe --withsql --withssh --documentroot /www --create --execute

Output

		##########################
		http://xxx.xxx.xxx.xxx/johndoe

		ssh :
		ip : xxx.xxx.xxx.xxx
		login : johndoe
		pass : Jf29ufOYALAL

		Database :
		http://xxx.xxx.xxx.xxx/phpmyadmin/
		login : johndoe
		pass : dD1M1TXEWGKX
		##########################

Create hosting without domain name but with ftp and mysql accounts

    ./managehosting --account johndoe --withsql --withftp --create --execute

Output

		##########################
		http://xxx.xxx.xxx.xxx/johndoe

		ftp :
		ip : xxx.xxx.xxx.xxx
		login : johndoe
		pass : Jf29ufOYALAL

		Database :
		http://xxx.xxx.xxx.xxx/phpmyadmin/
		login : johndoe
		pass : dD1M1TXEWGKX
		##########################


Delete hosting for the domain www.johndoe.com

    ./managehosting --account johndoe --domain www.johndoe.com --delete --execute

Output

		##########################

		Account johndoe and Domain www.johndoe.com deleted

		##########################

Get version

    ./managehosting -V

Output

    2016.06.29

Update to latest release

    ./managehosting -U

Output

    Updating to version 2016.06.30
    Updated managehosting. Restart managehosting to use the new version.