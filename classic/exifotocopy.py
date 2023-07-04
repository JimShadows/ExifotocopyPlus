#!/usr/bin/env python
#exifotocopy GTK frontend
#Jan 2010 hannenz@freenet.de

import pygtk
pygtk.require ('2.0')
import gtk
import sys
import re
import os
import subprocess


#Localisation Stuff
APP = 'exifotoconfig'
DIR = '%s/.exifotocopy/locale' % (os.getenv("HOME"))
import locale
import gettext
locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)
_=gettext.gettext

class ExiFotoConfig:
	appname = "exifotocopy"
	configfile = "%s/.exifotocopy/exifotocopyrc" % (os.getenv("HOME"))
	bashscript = "%s/bin/exifotocopy/exifotocopy.sh" % (os.getenv("HOME"))
	logofile = '%s/bin/exifotocopy/logo.png' % (os.getenv('HOME'))

	#execute bash script
	def run(self, widget, data=None):
		#save current settings to config file
		self.save(widget, data)
		
		#run script
		cmd = "%s \"%s\"" % (self.bashscript, self.srcdir_entry.get_text())
		try:
			retcode = subprocess.call(cmd, shell=True)
			if (retcode < 0):
				print >>sys.stderr, "child terminated by signal", -retcode
			else:
				print >>sys.stderr, "child returned", retcode
		except OSError, e:
			print >>sys.stderr, "execution failed:", e

		#~ gtk.main_quit()


	def filechooser(self, widget, icon_pos, event, title):
		fc = gtk.FileChooserDialog(
			title,
			None,
			gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK)
		)
		fc.set_default_response(gtk.RESPONSE_OK)
		fc.set_filename(widget.get_text())
		r = fc.run()
		if (r == gtk.RESPONSE_OK):
			widget.set_text(fc.get_filename())
		fc.destroy()

	def info(self, mssg):
		dlg = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, (gtk.BUTTONS_OK), mssg)
		dlg.run()
		dlg.destroy()

	def toggled2(self, widget, data=None):
		if (widget.get_active() == 0):
			self.fmtmonth_entry.set_sensitive(False)
			self.fmtday_entry.set_sensitive(False)
		elif (widget.get_active() == 1):
			self.fmtmonth_entry.set_sensitive(True)
			self.fmtday_entry.set_sensitive(False)
		elif (widget.get_active() == 2):
			self.fmtmonth_entry.set_sensitive(True)
			self.fmtday_entry.set_sensitive(True)

	def toggled3(self, widget, data=None):
		self.cmdopts_entry.set_sensitive(widget.get_active() == 2)

	def delete_event(self, widget, event, data=None):
		self.quit(widget, data)
		return False

	def destroy(self, widget, data=None):
		gtk.main_quit()

	#read bash variables from config file
	def read_bashvars(self):
		variables = {}
		f = open(self.configfile)
		lines = f.readlines()
		f.close()
		for line in lines:
			match = re.match('([a-zA-Z0-9_]+)="(.*)"', line)
			if (match):
				variables[match.group(1)] = match.group(2)
		return variables

	#save config file
	def save(self, widget, variables):
		f = open(self.configfile, "w+")
		f.write ("WANT_ZENITY=\"%u\"\n" % (1 if self.gui_entry.get_active() < 2 else 0))
		f.write ("NOTIFICATION=\"%u\"\n" % (1 if self.gui_entry.get_active() ==1 else 0))
		f.write ("EXTENSIONS=\"%s\"\n" % (self.extensions_entry.get_text()))
		f.write ("ASK=\"%u\"\n" % (0 if self.ask_entry.get_active() else 1))
		f.write ("PHOTOBASEDIR=\"%s\"\n" % (self.photobasedir_entry.get_text()))
		f.write ("DESTDEPTH=\"%u\"\n" % (self.destdepth_entry.get_active() + 1))
		f.write ("FMTYEAR=\"%s\"\n" % (self.fmtyear_entry.get_text()))
		f.write ("FMTMONTH=\"%s\"\n" % (self.fmtmonth_entry.get_text()))
		f.write ("FMTDAY=\"%s\"\n" % (self.fmtday_entry.get_text()))
		f.write ("FILEDATEFORMAT=\"%s\"\n" % (self.filedateformat_entry.get_text()))
		f.write ("NRFORMAT=\"%s\"\n" % (self.nrformat_entry.get_text()))
		cmd = self.cmd_entry.get_active()
		f.write ("CMD=\"%s\"\n" % ("cp" if cmd == 0 else "mv" if cmd == 1 else "convert"))
		f.write ("CMDOPTS=\"%s\"\n" % (self.cmdopts_entry.get_text()))
		f.write ("LOGFILE=\"%s\"\n" % (self.logfile_entry.get_text()))
		f.close()
		print _('Configuration saved.')

	def quit(self, widget, data):
		gtk.main_quit()

	def mlabel(self, text):
		l = gtk.Label()
		l.set_alignment(-1, 0.5)
		l.set_markup(text)
		return l

	def attach_to_table(self, label, widget, descr):
		tooltip = "<i>%s</i>" % (descr)
		l = self.mlabel(label)
		l.set_tooltip_markup(tooltip)
		widget.set_tooltip_markup(tooltip)
		self.table.attach(l, 0, 1, self.row, self.row + 1)
		self.table.attach(widget, 1, 2, self.row, self.row + 1)
		self.row = self.row + 1

	def entry_from_var(self, bashvar, label, tooltip):
		entry = gtk.Entry()
		entry.set_text(self.bashvars[bashvar])
		self.attach_to_table(label, entry, tooltip)
		return entry

	def __init__ (self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_border_width(10)
		self.window.set_title(self.appname)
		self.window.set_icon_from_file(self.logofile)
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)

		label = self.mlabel("<span size='x-large'><b>Exifotocopy</b></span>\nOrganize your image files by exif date")

		pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.logofile, 64, 64)
		logo = gtk.Image()
		logo.set_from_pixbuf(pixbuf)

		logobox = gtk.HBox()
		logobox.pack_start(logo, False, False, 0)
		logobox.pack_start(label, True, True, 10)

		white = gtk.gdk.Color(65535, 65535, 65535, 0)
		ebox = gtk.EventBox()
		#~ ebox.modify_bg(gtk.STATE_NORMAL, white)
		ebox.add(logobox)

		self.bashvars = self.read_bashvars()

		self.table = gtk.Table(13, 3, False)
		self.row = 0

		naut = os.getenv("NAUTILUS_SCRIPT_SELECTED_FILE_PATHS")
		if (naut != None):
			naut2 = naut.splitlines(False)
			self.srcdir = naut2[0]
		else:
			self.srcdir = os.getenv("PWD")

	
		self.srcdir_entry = gtk.Entry()
		self.srcdir_entry.set_icon_from_stock(gtk.ENTRY_ICON_SECONDARY, gtk.STOCK_DIRECTORY)
		self.srcdir_entry.set_text(self.srcdir)
		self.srcdir_entry.connect("icon-press", self.filechooser, _("Select source folder"))
		self.attach_to_table(
			_("Source Folder"),
			self.srcdir_entry,
			_("where to search for image files")
		)

		self.photobasedir_entry = gtk.Entry()
		self.photobasedir_entry.set_icon_from_stock(gtk.ENTRY_ICON_SECONDARY, gtk.STOCK_DIRECTORY)
		self.photobasedir_entry.set_text(self.bashvars['PHOTOBASEDIR'])
		self.photobasedir_entry.connect("icon-press", self.filechooser, _("Select destination folder"))
		self.attach_to_table(
			_("Destination Folder"),
			self.photobasedir_entry,
			_("default destination folder to use, if the above option is unset")
		)


		self.extensions_entry = self.entry_from_var(
			"EXTENSIONS",
			_("Filename Extensions"),
			_("a space seperated list of filename extensions (without the dot), the script should search for")
		)

		self.ask_entry = gtk.combo_box_new_text()
		self.ask_entry.append_text(_("Ask user"))
		self.ask_entry.append_text(_("Use the file's timestamp"))
		self.ask_entry.set_active(self.bashvars['ASK'] == "0")
		self.attach_to_table(
			_("No Exif Date Policy"),
			self.ask_entry,
			_("What to do if a file has no Exif Date")
		)

		self.destdepth_entry = gtk.combo_box_new_text()
		self.destdepth_entry.append_text("1")
		self.destdepth_entry.append_text("2")
		self.destdepth_entry.append_text("3")
		self.destdepth_entry.set_active(int(self.bashvars['DESTDEPTH']) - 1)
		self.destdepth_entry.connect("changed", self.toggled2)
		self.attach_to_table(
			_("Depth of Folder Structure"),
			self.destdepth_entry,
			_("Destination folder structur depth, determines how deeply nested the resulting destination folder structure will be, e.g. to sort your pictures by Year and Month, you could set this to '2', one folder for each year containing folders for each month of that year (where pictures are available)")
		)

		self.fmtyear_entry = self.entry_from_var('FMTYEAR',
			_("Format String Level 1 Folder"),
			_("Format string as passed to date command for the first directory level. Basic ones are:\n\n%d: day of month as number(1-31)\n%m: month as number (1-12)\n%B: month as localized string (e.g. 'March')\n%Y: Year \n%V: Calendar week (1-53)\n%H: Hour (0-23)\n%M: minute (0-59)\ni: Second (0-59)\n\nPlease refer to manpage of date command for more detailed info (type 'man date' in a terminal)")
		)

		self.fmtmonth_entry = self.entry_from_var('FMTMONTH',
			_("Format String Level 2 Folder"),
			_("Format string as passed to date command for the second directory level. Basic ones are:\n\n%d: day of month as number(1-31)\n%m: month as number (1-12)\n%B: month as localized string (e.g. 'March')\n%Y: Year \n%V: Calendar week (1-53)\n%H: Hour (0-23)\n%M: minute (0-59)\ni: Second (0-59)\n\nPlease refer to manpage of date command for more detailed info (type 'man date' in a terminal)")
		)

		self.fmtday_entry = self.entry_from_var('FMTDAY',
			_("Format String Level 3 Folder"),
			_("Format string as passed to date command for the third directory level. Basic ones are:\n\n%d: day of month as number(1-31)\n%m: month as number (1-12)\n%B: month as localized string (e.g. 'March')\n%Y: Year \n%V: Calendar week (1-53)\n%H: Hour (0-23)\n%M: minute (0-59)\ni: Second (0-59)\n\nPlease refer to manpage of date command for more detailed info (type 'man date' in a terminal)")
		)

		self.filedateformat_entry = self.entry_from_var('FILEDATEFORMAT',
			_("Format String Filename"),
			_("Format string as passed to date command for the destination filename. Basic ones are:\n\n%d: day of month as number(1-31)\n%m: month as number (1-12)\n%B: month as localized string (e.g. 'March')\n%Y: Year\n%V: Calendar week (1-53)\n%H: Hour (0-23)\n%M: minute (0-59)\ni: Second (0-59)\n\nPlease refer to manpage of date command for more detailed info (type 'man date' in a terminal)")
		)

		self.nrformat_entry = self.entry_from_var('NRFORMAT',
			_("Number Format String"),
			_("Format string as passed to printf command for the destination filename count. Leave blank to disable numbering, use printf-style format string, see manpage of printf for more detailed info (type 'man printf' in a terminal)")
		)

		self.cmd_entry = gtk.combo_box_new_text()
		self.cmd_entry.append_text(_("copied"))
		self.cmd_entry.append_text(_("moved"))
		self.cmd_entry.append_text(_("copied and resized"))
		if (self.bashvars['CMD'] == "cp"):
			self.cmd_entry.set_active(0)
		elif (self.bashvars['CMD'] == "mv"):
			self.cmd_entry.set_active(1)
		elif (self.bashvars['CMD'] == "convert"):
			self.cmd_entry.set_active(2)
		self.cmd_entry.connect("changed", self.toggled3)
		self.attach_to_table(
			_("Files will be"),
			self.cmd_entry,
			_("specify, what to do with each file")
		)

		self.cmdopts_entry = self.entry_from_var('CMDOPTS',
			_("convert options"),
			_("Any options 'convert' understands, e.g. to resize try something like '-resize 1280x800' or consult 'man convert'")
		)
		
		self.gui_entry = gtk.combo_box_new_text()
		self.gui_entry.append_text(_("Window"))
		self.gui_entry.append_text(_("Notification"))
		self.gui_entry.append_text(_("No GUI"))

		if (self.bashvars['WANT_ZENITY']):
			self.gui_entry.set_active(int(self.bashvars['NOTIFICATION']))
		else:
			self.gui_entry.set_active(2)

		self.attach_to_table(
			_("GUI Mode"),
			self.gui_entry,
			_("In window mode you will get a window with a progress bar, in notification mode an icon in the systray will keep you informed about the script's status")
		)

		self.logfile_entry = self.entry_from_var('LOGFILE',
			_("Logfile"),
			_("Location of logfile. Set to /dev/null to disable logging")
		)

		vbox = gtk.VBox(False, 6)
		vbox.pack_start(ebox, True, True, 10)
		vbox.add(gtk.HSeparator())
		vbox.add(self.table)
		vbox.add(gtk.HSeparator())

		hbox = gtk.HBox()
		quit_button = gtk.Button("", gtk.STOCK_QUIT)
		run_button = gtk.Button("", gtk.STOCK_EXECUTE)
		quit_button.connect("clicked", self.quit, self.bashvars)
		run_button.connect("clicked", self.run, self.bashvars)

		hbox.pack_start(quit_button, False, False, 0)
		hbox.pack_start(gtk.Label(""), True, True, 0)
		hbox.pack_start(run_button, False, False, 0)
		vbox.add(hbox)

		self.window.add(vbox)
		self.window.show_all()

		self.toggled2(self.destdepth_entry, None)
		self.toggled3(self.cmd_entry, None)

	def main(self):
		gtk.main()

if __name__ == "__main__":
	app = ExiFotoConfig()
	app.main()
