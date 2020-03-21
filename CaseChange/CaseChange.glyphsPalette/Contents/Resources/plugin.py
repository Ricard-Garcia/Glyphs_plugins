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

# Uppercaseable scripts
scriptsUC = ["latin", "cyrillic", "greek"]

class ChangeCase(PalettePlugin):

	def settings(self):
		self.name = "Change Case"
		# Create Vanilla window and group with controls
		width = 150
		height = 90
		self.paletteView = Window((width, height))
		self.paletteView.group = Group((0, 0, width, height))
		self.paletteView.group.UCButton = Button((10, -85, width-7, 20), "Uppercase", callback=self.changeCaseCallback_)
		self.paletteView.group.UCButton.getNSButton().setToolTip_(u"ABC Abc abc → ABC ABC ABC")
		self.paletteView.group.lcButton = Button((10, -60, width-7, 20), "Lowercase", callback=self.changeCaseCallback_)
		self.paletteView.group.lcButton.getNSButton().setToolTip_(u"ABC Abc abc → abc abc abc")
		self.paletteView.group.titleButton = Button((10, -35, width-7, 20), "Title", callback=self.changeCaseCallback_)
		self.paletteView.group.titleButton.getNSButton().setToolTip_(u"ABC Abc abc → Abc Abc Abc")

		# Set dialog to NSView
		self.dialog = self.paletteView.group.getNSView()
	
	def changeCaseCallback_(self, sender):
		Glyphs.clearLog()

		tab = self.windowController().activeEditViewController()

		# check if there is a tab open that contains text:
		if tab and tab.text:
			f = self.windowController().documentFont()

			currentLayers = tab.layers
			# Text to be used to replace the current text
			newText = ""
			for i, l in enumerate(currentLayers):

				# Glyph object
				g = l.parent
				
				# Avoid new line
				if g.name == None:
					newText += "\n"
					continue
				# **************************************************
				# Change case depending on which button was pressed:

				# UPPERCASE
				if sender == self.paletteView.group.UCButton:
					print("Uppercase text!")

					# Letter
					if g.category == "Letter" and g.script in scriptsUC:
						if g.script == "cyrillic":
							upperG = g.name[0].upper() + g.name[1:]
						else:
							upperG = g.name.title()

						newText += "/%s " % (upperG)

					# Number
					elif g.category == "Number" and g.name.replace('.osf', '') in f.glyphs:
						newText += "/%s " % (g.name.replace('.osf', ''))

					#everything else
					else:
						newText += "/%s " % (g.name)

				# LOWERCASE
				if sender == self.paletteView.group.lcButton:
					print("Lowercase text!")

					# Letter
					if g.category == "Letter" and g.script in scriptsUC:
						lowerG = g.name.lower()
						newText += "/%s " % (lowerG)

					# Number
					elif g.category == "Number" and g.name + ('.osf') in f.glyphs:
						newText += "/%s " % (g.name + ('.osf'))

					#everything else
					else:
						newText += "/%s " % (g.name)

				# TITLE
				if sender == self.paletteView.group.titleButton:
					print("Title text!")

					# Letter
					if g.category == "Letter" and g.script in scriptsUC:
						newName = g.name
						if i == 0:
							if g.script == "cyrillic":
								newName = g.name[0].upper() + g.name[1:]
							else:
								newName = g.name.title()
						else:
							newName = g.name.lower()
						newText += "/%s " % (newName)

					# Number
					elif g.category == "Number" and g.name + ('.osf') in f.glyphs:
						newText += "/%s " % (g.name + ('.osf'))

					#everything else
					else:
						newText += "/%s " % (g.name)

			# replace text in tab:
			tab.text = newText
