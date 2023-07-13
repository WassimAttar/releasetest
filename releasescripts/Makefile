clean:
	rm -rf managehosting managehosting.* managehosting.tar.gz ../build/
	find ../manage_hosting -name "*.pyc" -delete

PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin
PYTHON ?= /usr/bin/env python

install: managehosting
	install -d $(BINDIR)
	install -m 755 managehosting $(BINDIR)

managehosting.tar.gz:
	@tar -czf managehosting.tar.gz --owner 0 --group 0 \
		--exclude '*.pyc' \
		-- \
		../manage_hosting/*.py \
		../README.md \

managehosting:
	cd ../manage_hosting && \
	zip --quiet managehosting *.py && \
	echo '#!$(PYTHON)' > managehosting && \
	cat managehosting.zip >> managehosting && \
	rm managehosting.zip && \
	chmod a+x managehosting && \
	mv managehosting ../releasescripts/