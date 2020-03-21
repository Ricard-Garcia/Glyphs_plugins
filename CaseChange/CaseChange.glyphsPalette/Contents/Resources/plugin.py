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
				# **************************************************
				# Change case depending on which button was pressed:

				# UPPERCASE
				if sender == self.paletteView.group.UCButton:
					print("Uppercase text!")
					
					# If the character is not "latin" but still inside the category
					if g.script not in scriptsUC and g.category == "Letter":
						# Test
						print(g.name)

					# Avoid new line
					if l.parent.name == None:
						# Test
						print("New line!")
						newText += "\n"

					else:

						# All characters that are not letter or number
						if g.category not in changeCat:
							newText += "/%s " % (g.name)
					

						# Letter
						if g.script == "cyrillic":
							upperG = g.name[0].upper()+g.name[1:]
						else:
							upperG = g.name.title()

						if currentLayers[i-1].parent.category == "Separator" and g.category == "Letter":
							# Test
							#print("After space", upperG)
							newText += "/%s " % (upperG)

						elif g.category == "Letter":
							# Test
							#print(upperG)
							newText += "/%s " % (upperG)
					
							
						# Number
						if g.category == "Number":
							if g.name.replace('.osf','') in f.glyphs:
								# Test
								#print(g.name.replace('.osf',''))
								newText += "/%s " % (g.name.replace('.osf',''))
								
							else:
								# Test
								#print(g.name)
								newText += "/%s " % (g.name)




				# LOWERCASE
				if sender == self.paletteView.group.lcButton:
					print("Lowercase text!")
					
					# If the character is not "latin" but still inside the category
					if g.script not in scriptsUC and g.category == "Letter":
						# Test
						print(g.name)						

					# Avoid new line
					if l.parent.name == None:
						# Test
						print("New line!")
						newText += "\n"

					else:

						# All characters that are not letter or number
						if g.category not in changeCat:
							newText += "/%s " % (g.name)
					
						# Letter
						lowerG = g.name.lower()
						if currentLayers[i-1].parent.category == "Separator" and g.category == "Letter":
							# Test
							#print("After space", lowerG)
							newText += "/%s " % (lowerG)

						elif g.category == "Letter":
							# Test
							#print(lowerG)
							newText += "/%s " % (lowerG)
					
							
						# Number
						if g.category == "Number":
							if g.name+('.osf') in f.glyphs:
							
								# Test
								#print(g.name+('.osf'))
								newText += "/%s " % (g.name+('.osf'))
					
							else:
								# Test
								#print(g.name)
								newText += "/%s " % (g.name)


				# TITLE
				if sender == self.paletteView.group.titleButton:
					print("Title text!")
					
					# If the character is not "latin" but still inside the category
					if g.script not in scriptsUC and g.category == "Letter":
						# Test
						print(g.name)						

					# Avoid new line
					if l.parent.name == None:
						# Test
						print("New line!")
						newText += "\n"

					else:

						# All characters that are not letter or number
						if g.category not in changeCat:
							newText += "/%s " % (g.name)
					
					
						# Letter
						if g.script == "cyrillic":
							upperG = g.name[0].upper()+g.name[1:]
						else:
							upperG = g.name.title()

						lowerG = g.name.lower()

						# First character in text in uppercase
						if i == 0:
							newText += "/%s " % (upperG)

						if currentLayers[i-1].parent.category == "Separator" and g.category == "Letter":
							# Test
							#print("After space", upperG)
							newText += "/%s " % (upperG)

						elif g.category == "Letter":
							# First character has been already replaced and needs to be avoided
							if i == 0:
								pass

							else:
								# Test
								#print(lowerG)
								newText += "/%s " % (lowerG)
					
							
						# Number
						if g.category == "Number":
							if g.name+('.osf') in f.glyphs:
							
								# Test
								#print(g.name+('.osf'))
								newText += "/%s " % (g.name+('.osf'))
					
							else:
								# Test
								#print(g.name)
								newText += "/%s " % (g.name)






			# replace text in tab:
			tab.text = newText
