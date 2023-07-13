# coding: utf-8

import base64, json, mimetypes, netrc, argparse, os, urllib.request, getpass

def sanitize_url(url):
	return 'http:%s' % url if url.startswith('//') else url

def sanitized_Request(url, *args, **kwargs):
	return urllib.request.Request(sanitize_url(url), *args, **kwargs)

class GitHubReleaser():
	__API_URL = 'https://api.github.com/repos/WassimAttar/managehosting/releases'
	__UPLOADS_URL = 'https://uploads.github.com/repos/WassimAttar/managehosting/releases/%s/assets?name=%s'
	__NETRC_MACHINE = 'github.com'

	def __init__(self):
		self.__init_github_account()
		self.__opener = urllib.request.build_opener(urllib.request.HTTPSHandler)

	def __init_github_account(self):
		try:
			info = netrc.netrc().authenticators(self.__NETRC_MACHINE)
			if info is not None:
				self.__username = info[0]
				self.__password = info[2]
				print('Using GitHub credentials found in .netrc...')
				return
			else:
				print('No GitHub credentials found in .netrc')
		except (IOError, netrc.NetrcParseError):
			print('Unable to parse .netrc')
		self.__username = input('Type your GitHub username or email address and press [Return]: ')
		self.__password = getpass.getpass('Type your GitHub password and press [Return]: ')

	def __call(self, req):
		if isinstance(req, str):
			req = sanitized_Request(req)
		b64 = base64.b64encode(('%s:%s' % (self.__username, self.__password)).encode('utf-8')).decode('ascii')
		req.add_header('Authorization', 'Basic %s' % b64)
		response = self.__opener.open(req).read().decode('utf-8')
		return json.loads(response)

	def create_release(self, tag_name, name):
		data = {
				'tag_name': tag_name,
				'target_commitish': 'master',
				'name': name,
				'body': '',
				'draft': False,
				'prerelease': False,
		}
		req = sanitized_Request(self.__API_URL, json.dumps(data).encode('utf-8'))
		return self.__call(req)

	def create_asset(self, release_id, asset):
		asset_name = os.path.basename(asset)
		url = self.__UPLOADS_URL % (release_id, asset_name)
		data = open(asset, 'rb').read()
		req = sanitized_Request(url, data)
		mime_type, _ = mimetypes.guess_type(asset_name)
		req.add_header('Content-Type', mime_type or 'application/octet-stream')
		return self.__call(req)


def main():
	parser = argparse.ArgumentParser(description='Release to Github')
	parser.add_argument('version', type=str, default="", help='Release Version')
	parser.add_argument('build_path', type=str, default="", help='Build Path')
	args = parser.parse_args()

	version = args.version
	build_path = args.build_path

	releaser = GitHubReleaser()

	new_release = releaser.create_release(version, name='managehosting %s' % version)
	release_id = new_release['id']

	for asset in os.listdir(build_path):
		print('Uploading %s...' % asset)
		releaser.create_asset(release_id, os.path.join(build_path, asset))


if __name__ == '__main__':
	main()