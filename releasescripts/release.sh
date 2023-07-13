#!/bin/bash

set -e

if [ -z "$1" ]; then echo "ERROR: specify version number like this: $0 1994.09.06"; exit 1; fi
version="$1"
major_version=$(echo "$version" | sed -n 's#^\([0-9]*\.[0-9]*\.[0-9]*\).*#\1#p')
if test "$major_version" '!=' "$(date '+%Y.%m.%d')"; then
    echo "$version does not start with today's date!"
    exit 1
fi

if [ ! -z "`git tag | grep "$version"`" ]; then echo 'ERROR: version already present'; exit 1; fi
if [ ! -z "`git status --porcelain | grep -v CHANGELOG`" ]; then echo 'ERROR: the working directory is not clean; commit or stash changes'; exit 1; fi
useless_files=$(find manage_hosting/ -type f -not -name '*.py')
if [ ! -z "$useless_files" ]; then echo "ERROR: Non-.py files in managehosting: $useless_files"; exit 1; fi

/bin/echo -e "\n### Changing version in version.py..."
sed -i "s/__version__ = '.*'/__version__ = '$version'/" manage_hosting/version.py

/bin/echo -e "\n### Committing version.py..."
git add manage_hosting/version.py
git commit -m "release $version"

/bin/echo -e "\n### Now tagging, signing and pushing..."
git tag -s -m "Release $version" "$version"
git show "$version"
read -p "Is it good, can I push? (y/n) " -n 1
if [[ ! $REPLY =~ ^[Yy]$ ]]; then exit 1; fi
echo
MASTER=$(git rev-parse --abbrev-ref HEAD)
git push origin $MASTER:master
git push origin "$version"

/bin/echo -e "\n### OK, now it is time to build the binaries..."
REV=$(git rev-parse HEAD)
(cd releasescripts/ && make managehosting managehosting.tar.gz)
mkdir -p "build/$version"
mv releasescripts/managehosting "build/$version"
mv releasescripts/managehosting.tar.gz "build/$version/managehosting-$version.tar.gz"
RELEASE_FILES="managehosting managehosting-$version.tar.gz"
(cd build/$version/ && md5sum $RELEASE_FILES > MD5SUMS)
(cd build/$version/ && sha1sum $RELEASE_FILES > SHA1SUMS)
(cd build/$version/ && sha256sum $RELEASE_FILES > SHA2-256SUMS)
(cd build/$version/ && sha512sum $RELEASE_FILES > SHA2-512SUMS)

/bin/echo -e "\n### Signing and uploading the new binaries to GitHub..."
for f in $RELEASE_FILES; do gpg --passphrase-repeat 5 --detach-sig "build/$version/$f"; done

ROOT=$(pwd)
python3 releasescripts/create-github-release.py $version "$ROOT/build/$version"

rm -rf build
(cd releasescripts/ && make clean)

/bin/echo -e "\n### DONE!"