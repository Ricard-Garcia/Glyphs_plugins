# encoding: utf-8

###########################################################################################################
#
#
#	Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################

from GlyphsApp.plugins import *
from vanilla import *


class ChangeCase(PalettePlugin):

	def settings(self):

		self.name = "Change Case"

		# Create Vanilla window and group with controls
		width = 150
		height = 90
		self.paletteView = Window((width, height))
		self.paletteView.group = Group((0, 0, width, height))
		self.paletteView.group.UCButton = Button((10, -85, width-7, 20), "Uppercase", callback=self.upperCallback)
		self.paletteView.group.UCButton.getNSButton().setToolTip_(u"ABC Abc abc → ABC ABC ABC")
		self.paletteView.group.lcButton = Button((10, -60, width-7, 20), "Lowercase", callback=self.lowerCallback)
		self.paletteView.group.lcButton.getNSButton().setToolTip_(u"ABC Abc abc → abc abc abc")
		self.paletteView.group.titleButton = Button((10, -35, width-7, 20), "Title", callback=self.titleCallback)
		self.paletteView.group.titleButton.getNSButton().setToolTip_(u"ABC Abc abc → Abc Abc Abc")
		
		# Set dialog to NSView
		self.dialog = self.paletteView.group.getNSView()

			
	# Uppercase
	def upperCallback(self, sender):
		windowController = self.windowController()
		if windowController:
			thisFont = windowController.document().font
			if thisFont.currentText:
				thisFont.currentText = thisFont.currentText.upper()
		
	# Lowercase
	def lowerCallback(self, sender):
		windowController = self.windowController()
		if windowController:
			thisFont = windowController.document().font
			if thisFont.currentText:
				thisFont.currentText = thisFont.currentText.lower()
	
	# Title
	def titleCallback(self, sender):
		windowController = self.windowController()
		if windowController:
			thisFont = windowController.document().font
			if thisFont.currentText:
				thisFont.currentText = thisFont.currentText.title()



