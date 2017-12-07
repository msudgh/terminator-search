#!/usr/bin/python
from terminatorlib import plugin, config
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from subprocess import call

AVAILABLE = ['TerminatorSearch']

class TerminatorSearch(plugin.MenuItem):
  capabilities = ['terminal_menu']

  def __init__(self):
    self.plugin_name = self.__class__.__name__
    self.clipboard = None
    self.content = None

  def callback(self, menuitems, menu, terminal):
    # retrive the context of clipboard
    self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
    self.content = self.clipboard.wait_for_text()

    # extract 5 character of the clipboard
    content_summary = self.content[0:10].strip()

    # make available search item in context menu if the clipboard isn't empty
    if len(content_summary) > 0 and content_summary != None:
      self.add_submenu(menu, ('Search For %s...' % (content_summary)), terminal)

  def add_submenu(self, submenu, name, terminal):
    # create menu item
    menu = Gtk.MenuItem(name)

    # call on_click method while Clicking on menu item
    menu.connect("activate", self.on_click, terminal)

    # append menu item to context menu
    submenu.append(menu)
    return menu

  def on_click(self, widget, event):
    url = 'https://www.google.com/search?q=' + self.content
    call(["xdg-open", url])
