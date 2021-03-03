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
from vanilla import Window, Button, Group

# Casefolding scripts:
scriptsUC = (
	"latin",
	"cyrillic",
	"greek",
	"armenian",
	"georgian",
	"adlam",
	"coptic",
	"glagolitic",
	"rovas",
	)

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
	
	@objc.python_method
	def casefoldChar(self, thisChar, case="lower"):
		if case=="upper":
			return thisChar.upper()
		return thisChar.lower()
	
	@objc.python_method
	def separateCoreFromSuffix(self, glyphName):
		if "." in glyphName:
			firstPart = glyphName[:glyphName.find(".")]
			secondPart = glyphName[glyphName.find("."):]
			return firstPart, secondPart
		else:
			return glyphName, ""
	
	@objc.python_method
	def glyphNameForCase(self, glyphName, case="lower"):
		thisChar = Glyphs.glyphInfoForName(glyphName).unicharString()
		if thisChar:
			casefoldedChar = self.casefoldChar(thisChar, case=case)
			casefoldedGlyphName = Glyphs.niceGlyphName(casefoldedChar)
			return casefoldedGlyphName
		elif "." in glyphName[1:] and glyphName[0]!=".":
			coreGlyphName, suffix = self.separateCoreFromSuffix(glyphName)
			caseFoldedCoreGlyphName = self.glyphNameForCase(coreGlyphName, case)
			return caseFoldedCoreGlyphName+suffix
		else:
			# cannot casefold
			return glyphName
	
	def changeCaseCallback_(self, sender):
		if Glyphs.defaults["com.RicardGarcia.ChangeCase.verboseReport"]:
			Glyphs.clearLog()

		tab = self.windowController().activeEditViewController()

		# check if there is a tab open that contains text:
		if tab and tab.text:
			f = self.windowController().documentFont()
			previousGlyphTypeIsSeparator = True
			currentLayers = tab.layers
			# Text to be used to replace the current text
			newText = ""
			for i, l in enumerate(currentLayers):
				# Glyph object
				g = l.parent
				
				# Avoid new line:
				if g.name == None:
					newText += "\n"
					previousGlyphTypeIsSeparator = True
					continue
				
				# Skip non-letters relevant for title case:
				if g.category in ("Separator", "Symbol", "Punctuation", "Mark", "Icon"):
					newText += "/%s" % g.name
					previousGlyphTypeIsSeparator = True
					continue

				# **************************************************
				# Change case depending on which button was pressed:

				# UPPERCASE
				if sender == self.paletteView.group.UCButton:
					if Glyphs.defaults["com.RicardGarcia.ChangeCase.verboseReport"]:
						print("Uppercase: %s"%g.name)

					# Letter
					if g.category == "Letter" and g.script in scriptsUC:
						newGlyphName = self.glyphNameForCase(g.name, case="upper")
						if not f.glyphs[newGlyphName]:
							# leave it if casefolded version does not exist:
							newGlyphName = g.name
						newText += "/%s " % (newGlyphName)

					# Number
					elif g.category == "Number" and f.glyphs[g.name.replace('.osf', '').replace('.tosf','.tf')]:
						newText += "/%s " % (g.name.replace('.osf', '').replace('.tosf','.tf'))

					#everything else
					else:
						newText += "/%s " % (g.name)

				# LOWERCASE
				elif sender == self.paletteView.group.lcButton:
					if Glyphs.defaults["com.RicardGarcia.ChangeCase.verboseReport"]:
						print("Lowercase: %s"%g.name)

					# Letter
					if g.category == "Letter" and g.script in scriptsUC:
						newGlyphName = self.glyphNameForCase(g.name, case="lower")
						if not f.glyphs[newGlyphName]:
							# leave it if casefolded version does not exist:
							newGlyphName = g.name
						newText += "/%s " % (newGlyphName)

					# Number
					elif g.category == "Number" and f.glyphs[g.name+'.osf']:
						newText += "/%s " % (g.name+'.osf')

					#everything else
					else:
						newText += "/%s " % (g.name)

				# TITLE
				elif sender == self.paletteView.group.titleButton:
					if Glyphs.defaults["com.RicardGarcia.ChangeCase.verboseReport"]:
						print("Title: %s"%g.name)

					# Letter
					if g.category == "Letter" and g.script in scriptsUC:
						newName = g.name
						if previousGlyphTypeIsSeparator:
							casefoldTarget = "upper"
						else:
							casefoldTarget = "lower"
						
						newGlyphName = self.glyphNameForCase(g.name, case=casefoldTarget)
						if not f.glyphs[newGlyphName]:
							# leave it if casefolded version does not exist:
							newGlyphName = g.name
						newText += "/%s " % (newGlyphName)

					# Number
					elif g.category == "Number" and f.glyphs[g.name+'.osf']:
						newText += "/%s " % (g.name+'.osf')

					#everything else
					else:
						newText += "/%s " % (g.name)
				
				previousGlyphTypeIsSeparator = False
				
			# replace text in tab:
			tab.text = newText
