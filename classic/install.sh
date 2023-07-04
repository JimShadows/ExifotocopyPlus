#!/bin/bash

DEST=${2:-"${HOME}/bin/exifotocopy"}
NAUT="${HOME}/.gnome2/nautilus-scripts"
NAUTDEST="${NAUT}/exifotocopy"
RC="${HOME}/.exifotocopy"

function install {
	(
		[ -d "${DEST}" ] || mkdir -p "${DEST}"
		cp exifotocopy.* logo.png "${DEST}"
		chmod +x "${DEST}/exifotocopy."*

		[ -d "${RC}" ] || mkdir "${RC}"
		cp ./defaultcfg "${RC}/exifotocopyrc"
		[ -d "${RC}/locale/de/LC_MESSAGES" ] || mkdir -p "${RC}/locale/de/LC_MESSAGES"
		cp locale/de/LC_MESSAGES/exifotoconfig.mo "${RC}/locale/de/LC_MESSAGES"
	) && echo "successfully installed to $DEST" || echo "failed to install to ${DEST}"
	which jhead >/dev/null|| echo "jhead is not installed. Please install jhead in order to use exifotocopy"
}

function install-nautilus {
	[ -x "${DEST}/exifotocopy.py" ] && ln -sf "${DEST}/exifotocopy.py" "${NAUT}/ExiFotoCopy" && echo "successfully installed to Nautilus Scripts" || echo "failed to install to Nautilus Scripts"
	which zenity >/dev/null || echo "zenity is not installed, but recommended if exifotocopy shall run as nautilus-script. Consider installing zenity"
	python -c "import pygtk,gtk; print 'gtk version (>=2.16 needed) is: ',gtk.gtk_version" || "python/PyGTK is not installed, but recommended if exifotocopy shall run as nautilus-script. Consider installing python and pygtk (GTK >= 2.16)"
}

function uninstall {
	(
	rm -f "${NAUT}/ExiFotoCopy"
	rm -rf ${DEST}
	rm -rf ${RC}
	) && echo "uninstalled successfully" || echo "failed to uninstall"
}

function usage {
	echo "usage: ${0} install|nautilus|uninstall [dest]"
	echo ""
	echo "install:   install to [dest], defaults to ~/bin"
	echo "nautilus:  install to [dest] and put symbolic links into nautilus-scripts-directory"
	echo "uninstall: remove all installed files"
	echo ""
}

ACTION=${1:-nautilus}

case ${ACTION} in
	"help")
		usage
		;;
	"install")
		install
		;;
	"nautilus")
		install
		install-nautilus
		;;
	"uninstall")
		uninstall
		;;
	*)
		usage
esac
