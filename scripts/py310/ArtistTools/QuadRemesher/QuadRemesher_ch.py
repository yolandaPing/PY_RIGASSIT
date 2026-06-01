
# encoding:utf-8

import subprocess
import os
import sys
import platform
import shutil
import tempfile
import time
import webbrowser  
import re 

from maya import OpenMayaUI as OpenMayaUI_1  # API 1.0

import maya.cmds as cmds

isVersionBeforeMaya2017 = False
mayaMajorVersion = 0
try:
	mayaMajorVersion = int(cmds.about(version=True)[0:4])
	if mayaMajorVersion < 2017:   # this line may generate an exception with beta version...
		isVersionBeforeMaya2017 = True
except Exception:
	sys.stdout.write("cannot extract version number...\n")

if isVersionBeforeMaya2017:
	from PySide.QtCore import *
	from PySide.QtGui import *
	from PySide.QtUiTools import *
	from shiboken import wrapInstance
else:
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtUiTools import *
	from PySide2.QtWidgets import *
	from shiboken2 import wrapInstance
	
import maya.mel as mel

def maya_useNewAPI():
	"""
	The presence of this function tells Maya that the plugin produces, and
	expects to be passed, objects created using the Maya Python API 2.0.
	"""
	pass


verboseDebug = False


def unixifyPath(path):
	path = path.replace('\\', '/')
	return path

# persistent vars:
def getOptionVarInt(id, default):
	if (mel.eval('optionVar -exists "%s"' % id)):
		return int(mel.eval('optionVar -q "%s"' % id))
	return default

def getOptionVarFloat(id, default):
	if (mel.eval('optionVar -exists "%s"' % id)):
		return float(mel.eval('optionVar -q "%s"' % id))
	return default

def getOptionVarBool(id, default):
	if (getOptionVarInt(id, default) != 0):
		return True
	return False

def setOptionVarInt(id, value):
	mel.eval('optionVar -iv "%s" %d' % (id, value))

def setOptionVarFloat(id, value):
	mel.eval('optionVar -fv "%s" %f' % (id, value))

def setOptionVarBool(id, value):
	setOptionVarInt(id, value)



# -------------------------------------- Window  -----------------------
class QuadRemesherWindow(QWidget):
	theWindow=None

	lang = {"en",()}

	def __init__(self, *args, **kwargs):
		super(QuadRemesherWindow, self).__init__(*args, **kwargs)

		self.language = 'Chinese'
		
		mayaMainWindowPtr = OpenMayaUI_1.MQtUtil.mainWindow()
		if sys.version_info.major > 2:
			mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QMainWindow)
		else:
			mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QMainWindow)
		#print(" mayaMainWindow = %s..\n" % str(mayaMainWindow))

		try:
			self.setParent(mayaMainWindow)
			self.setWindowFlags(Qt.Window)
			self.setObjectName('QuadRemesherWindow_uniqueId')

			# Makes Maya perform magic which makes the window stay on top in OS X and Linux.
			# And, it'll make Maya remember the window position
			self.setProperty("saveWindowPref", True)

			#qrBETA = ' (B8)'
			qrBETA = '' # Candidate Release!
			self.setWindowTitle('Quad Remesher 1.0.1' + qrBETA)
			self.setGeometry(200, 150, 300, 320)
			self.initUI()
			
		except Exception:
			sys.stdout.write("Execption: init..\n")
		
	# NB: initUI is called inside try catch... no need to add more here
	def initUI(self):
		posY = 20
		
		mainLayout = QVBoxLayout()
		self.setLayout(mainLayout)
	
		# -- tooltips: --
		curvatureAdaptivness_Tooltip = "Allows to control how quad's size locally adapts to curvatures.\nThe higher it is, the smaller the quads will be on high curvature areas.\nSet it at 0, to get uniform quads size"
		adaptQuadCount_Tooltip = "Adaptive Quad-Count :\nChecked: Creates more polygons than asked to fit high curvatures area. \nUnChecked(default): Respect the Target-Quad-Count more exactly.\nIt's advised to let it Unchecked to better respect the Target-Quad-Count. see the doc for more explanations. "
		useVertexColors_Tooltip = "Use 'Vertex Colors' to control Quads size density."
		vertexColorWidget_Tooltip = "Defines the Color to paint to control locally the desired Quad Density variations (using 'Paint Vertex Color Tool' in RGB mode) \n . from 0.25 => 'divide density by 4'  =  Big Quads  =  Cyan color \n . to 4  => 'multiply density by 4'  =  Small Quads  =  Red color."
		useMaterials_Tooltip="If On, QuadRemesher will use existing 'Materials' to guide the quad remeshing on Materials borders.\nMaterialIds will be maintained after remeshing."
		useHardEdges_Tooltip="If On, QuadRemesher will use existing 'Harden/Soften Edges' to guide the quad remeshing.\nAs Boolean operations automatically set the Hard/Soft edges, it's advised to enable it in case of Boolean results remeshing."
		useNormalsCreasing="If On, QuadRemesher will use the existing 'Normals' to guide the remeshing on edge loops where the normals are creased.\nAs most operations automatically set the Normals, it's advised to enable it.\nOn smooth organic shapes, it's advises to uncheck it."
		detectHardEdges_Tooltip="If On, QuadRemesher will detect/compute Hard-Edges automatically based on the geometry (using a mix of edge's angles and other geometrical considerations).\nThis is useful is you have not defined some Harden/Soften edges and if you want QuadRemesher to find hard angles automatically.\nIf 'Use existing Hard/Soft Edges' is checked, it's better to uncheck 'Detect Hard Edges'.\nOn smooth organic shapes, it's advises to uncheck it."
		symToolTip = "These options allows to perform symmetrical quad remeshing. It's possible to combine all 3 symmetry axis.\nTAKE CARE: The axis are Local Coordinates axis! It's advised to set the Gizmo in 'Object' mode to better see the Local Coordinates axis."
		remeshButton_Tooltip = "Performs the quad remeshing of the selected mesh."

		# -- TargetQuadCount line --
		hbox = QHBoxLayout()
		mainLayout.addLayout(hbox)
		
		self.label1 = QLabel()
		self.label1.setText("目标四边面数量")
		#self.label1.move(20, posY)
		hbox.addWidget(self.label1)
		
		self.targetQuadCountSpinBox = QSpinBox()
		self.targetQuadCountSpinBox.setRange(4, 1000000)
		self.targetQuadCountSpinBox.setValue( getOptionVarInt("QRtargetQuadCount", 5000) )
		self.targetQuadCountSpinBox.setSingleStep(100)
		self.targetQuadCountSpinBox.setToolTip("Set the desired number of Quads")
		hbox.addWidget(self.targetQuadCountSpinBox)
		
		# --- Quads Sizing Group ---
		self.groupBox1 = QGroupBox("四边面大小设置 ...", self)
		groupVLayout = QVBoxLayout()
		self.groupBox1.setLayout(groupVLayout)
		mainLayout.addWidget(self.groupBox1)
		
		hbox = QHBoxLayout()
		groupVLayout.addLayout(hbox)
		
		self.label2 = QLabel()
		self.label2.setText("自适应大小")
		hbox.addWidget(self.label2)
		
		self.curvatureAdaptivnessSpinBox = QSpinBox()
		self.curvatureAdaptivnessSpinBox.setRange(0, 100)
		self.curvatureAdaptivnessSpinBox.setValue( getOptionVarInt("QRcurvatureAdaptivness", 50) )
		self.curvatureAdaptivnessSpinBox.setSingleStep(1)	
		self.curvatureAdaptivnessSpinBox.setToolTip(curvatureAdaptivness_Tooltip)
		hbox.addWidget(self.curvatureAdaptivnessSpinBox)
		
		self.adaptQuadCount = QCheckBox()
		self.adaptQuadCount.setText("自适应四边化数量")
		self.adaptQuadCount.setChecked( getOptionVarBool("QRadaptQuadCount", False) ) 
		self.adaptQuadCount.setToolTip(adaptQuadCount_Tooltip)
		groupVLayout.addWidget(self.adaptQuadCount)
		
		groupVLayout.addStretch(6)
      
		self.useVertexColor = QCheckBox()
		self.useVertexColor.setText("使用顶点色表示四边化强度")
		self.useVertexColor.setChecked( getOptionVarBool("QRuseVertexColor", False) ) 
		self.useVertexColor.setToolTip(useVertexColors_Tooltip)
		groupVLayout.addWidget(self.useVertexColor)
      
		hbox = QHBoxLayout()
		groupVLayout.addLayout(hbox)
		
		self.label3 = QLabel()
		self.label3.setText("四边化强度(绘制)")
		hbox.addWidget(self.label3)
		
		self.vertexColorWidget = QDoubleSpinBox()
		self.vertexColorWidget.setRange(0.25, 4)
		self.vertexColorWidget.setValue( getOptionVarFloat("QRvertexColorValue", 1.0) )
		self.vertexColorWidget.setSingleStep(0.05)
		self.vertexColorWidget.setToolTip(vertexColorWidget_Tooltip)
		self.label3.setToolTip(vertexColorWidget_Tooltip)
		self.vertexColorWidget.valueChanged.connect(self.vertexColorWidget_valueChanged)
		hbox.addWidget(self.vertexColorWidget)


		# ---- Edge Loops Control... group: ----
		self.groupBox2 = QGroupBox("循环边控制 ...", self)
		groupVLayout = QVBoxLayout()
		self.groupBox2.setLayout(groupVLayout)
		mainLayout.addWidget(self.groupBox2)
		
		self.useMaterials = QCheckBox()
		self.useMaterials.setText("使用材质")
		self.useMaterials.setToolTip(useMaterials_Tooltip)
		self.useMaterials.setChecked( getOptionVarBool("QRuseMaterials", False) ) 
		groupVLayout.addWidget(self.useMaterials)
		
		self.useHardEdges = QCheckBox()
		self.useHardEdges.setText("使用已存在的 硬边/软边")
		self.useHardEdges.setToolTip(useHardEdges_Tooltip)
		self.useHardEdges.setChecked( getOptionVarBool("QRuseHardEdges", False) ) 
		groupVLayout.addWidget(self.useHardEdges)
		
		self.useIndexedNormals = QCheckBox()
		self.useIndexedNormals.setText("使用法线折痕")
		self.useIndexedNormals.setToolTip(useNormalsCreasing)
		self.useIndexedNormals.setChecked( getOptionVarBool("QRuseIndexedNormals", False) ) 
		groupVLayout.addWidget(self.useIndexedNormals)
		
		self.autoDetectHardEdges = QCheckBox()
		self.autoDetectHardEdges.setText("按角度检测硬边")
		self.autoDetectHardEdges.setToolTip(detectHardEdges_Tooltip)
		self.autoDetectHardEdges.setChecked( getOptionVarBool("QRautoDetectHardEdges", True) ) 
		groupVLayout.addWidget(self.autoDetectHardEdges)
		
		# ---- Misc... group: ----
		self.groupBox3 = QGroupBox("杂项 ...", self)
		groupVLayout = QVBoxLayout()
		self.groupBox3.setLayout(groupVLayout)
		mainLayout.addWidget(self.groupBox3)
		
		# - Symmetry -
		''' old symmetry
		self.symmetry = QCheckBox()
		self.symmetry.setText("Use symmetry options")
		self.symmetry.setToolTip('Use Maya Symmetry Options to perform a symmetrical remeshing.')
		self.symmetry.setChecked( getOptionVarBool("QRsymmetry", False) ) 
		groupVLayout.addWidget(self.symmetry)
		'''
		symHLayout = QHBoxLayout()
		groupVLayout.addLayout(symHLayout)
		
		self.symLabel = QLabel()
		self.symLabel.setText("对称 : ")
		self.symLabel.setToolTip(symToolTip)
		symHLayout.addWidget( self.symLabel )
		
		self.symmetry_x = QCheckBox()
		self.symmetry_x.setText("X")
		self.symmetry_x.setToolTip(symToolTip)
		self.symmetry_x.setChecked( getOptionVarBool("QRsymmetry_x", False) ) 
		symHLayout.addWidget( self.symmetry_x )
		
		self.symmetry_y = QCheckBox()
		self.symmetry_y.setText("Y")
		self.symmetry_y.setToolTip(symToolTip)
		self.symmetry_y.setChecked( getOptionVarBool("QRsymmetry_y", False) ) 
		symHLayout.addWidget( self.symmetry_y )
		
		self.symmetry_z = QCheckBox()
		self.symmetry_z.setText("Z")
		self.symmetry_z.setToolTip(symToolTip)
		self.symmetry_z.setChecked( getOptionVarBool("QRsymmetry_z", False) ) 
		symHLayout.addWidget( self.symmetry_z )
				
		# - licManager -
		mgrDoc_HLayout = QHBoxLayout()
		groupVLayout.addLayout(mgrDoc_HLayout)

		self.languageButton = QPushButton()
		self.languageButton.setText('语言')
		self.languageButton.clicked.connect(self.switch_language)
		self.languageButton.setFixedHeight(20)
		mgrDoc_HLayout.addWidget(self.languageButton)
		
		self.licManagerButton = QPushButton()
		self.licManagerButton.setText('许可证管理器')
		self.licManagerButton.clicked.connect(self.licenseManagerButton_onClicked)
		#self.licManagerButton.setSizeIncrement(0, -5) # does not work
		self.licManagerButton.setFixedHeight( 20 )
		#self.licManagerButton.setFixedHeight( self.licManagerButton.height()-5 ) # does not work...
		mgrDoc_HLayout.addWidget(self.licManagerButton)
		
		self.webDocButton = QPushButton()
		self.webDocButton.setText('帮助')
		self.webDocButton.clicked.connect(self.webDocButton_onClicked)
		self.webDocButton.setFixedHeight( 20 )
		mgrDoc_HLayout.addWidget(self.webDocButton)
		
		# -- News button --
		self.newVerText = None
		self.newVerUrl = None
		newsFileLines = None
		try:
			# read the news file
			newsFilePath = os.path.join(os.getenv('LOCALAPPDATA'), "Exoside/QuadRemesher/Datas_Maya/ServerNews.txt")
			if (verboseDebug):
				sys.stdout.write("newsFilePath = "+newsFilePath+"\n")
			f = open(newsFilePath, "r")
			newsFileLines = f.read().split("\n")
			f.close()
			if (verboseDebug):
				sys.stdout.write("newsFileLines = "+str(newsFileLines)+"\n")
		except Exception:
			self.newVerUrl = None # no serverNews file!
			
		try:
			# add the button		
			if (newsFileLines!=None) and (len(newsFileLines)>=2):
				self.newVerText = newsFileLines[0]
				self.newVerUrl = newsFileLines[1]
				
				self.newVerButton = QPushButton()
				self.newVerButton.setText(self.newVerText)
				self.newVerButton.setToolTip('open url : ' + self.newVerUrl)
				self.newVerButton.clicked.connect(self.newVerButton_onClicked)
				groupVLayout.addWidget(self.newVerButton)
		except Exception:
			import traceback
			sys.stdout.write("Error while adding news button : \n" + str(traceback.format_exc())+"\n")
		
		# --- "Remesh It" button ---
		self.remeshButton = QPushButton()
		self.remeshButton.setText('<<   REMESH IT   >>')
		self.remeshButton.setToolTip(remeshButton_Tooltip)
		font = self.remeshButton.font()
		font.setBold(True)
		if font.pointSize()>0:
			font.setPointSize(font.pointSize()*1.25)
		elif font.pixelSize()>0:
			font.setPixelSize(font.pixelSize()*1.25)
		self.remeshButton.setFont(font)
		#self.remeshButton.setMinimumHeight( self.remeshButton.minimumHeight() + 10  )
		self.remeshButton.setFixedHeight( 35 )
		#self.remeshButton.setSizeIncrement(0, 55) # does not work!
		self.remeshButton.clicked.connect(self.remeshButton_onClicked)
		mainLayout.addWidget(self.remeshButton)


	def vertexColorWidget_valueChanged(self): # -------------------- ColorSlider Changed ---------------
		try:
			vertexColorSliderValue = self.vertexColorWidget.value()
			#sys.stdout.write("vertexColorSliderValue: %f \n" % vertexColorSliderValue)
			
			# -- Slider Values mapping:
			# Mapping1 : slider in [-1, 1]
			# normalizedValue = vertexColorSliderValue

			#Mapping2: Slider in [0.25, 4]
			maxSliderValue = 4
			minSliderValue = 0.25
			normalizedValue = 0.0
			if vertexColorSliderValue > 1.0:
				normalizedValue = (vertexColorSliderValue - 1.0) / (maxSliderValue - 1.0)
			elif vertexColorSliderValue < 1.0:
				normalizedValue =  - ((1.0/vertexColorSliderValue) - 1.0) / ((1.0/minSliderValue) - 1.0)

			if (normalizedValue > 1):
				normalizedValue = 1
			if (normalizedValue < -1):
				normalizedValue = -1

			# -- normalizedValue to color
			r = 1.0
			g = 1.0
			b = 1.0
			if normalizedValue > 0.0:
				r = 1
				g = 1-normalizedValue
				b = 1-normalizedValue
			elif normalizedValue < 0.0:
				r = 1+normalizedValue
				g = 1
				b = 1
		except Exception:
			sys.stdout.write("Exception: in vertexColorWidget_valueChanged..\n")
			
		try:
			mel.eval("artAttrPaintVertexCtx -e -colorRGBValue %f %f %f `currentCtx`;" % (r, g, b))
		except Exception:
			# if the tool is not loaded.... it generates an exception... 
			#sys.stdout.write("Exception: in vertexColorWidget_valueChanged..\n")
			b=0

		
		

	def remeshButton_onClicked(self): # ---------------------------------------------- Do REMESH FUNC -----------------------
		try:
			# environment settings
			maya_install_folder = os.getenv("MAYA_LOCATION")
			script_folder = os.path.dirname(os.path.realpath(__file__))

			# 0 -- it need fbxplugin loaded:
			fbxWasLoaded = mel.eval('pluginInfo -q -loaded "fbxmaya.mll"')
			if (fbxWasLoaded == 0) :
				print ("Loading FBX plugin for QuadRemesher...\n")
				mel.eval('loadPlugin "fbxmaya.mll"')

			''' start testing/using ExoMesh loader 				
			# 0.b -- it need QuadRemesher plugin loaded: (for ExoMesh import)
			QRWasLoaded = mel.eval('pluginInfo -q -loaded "QuadRemesherPlugIn.py"')
			if (QRWasLoaded == 0) :
				print ("Loading QuadRemesherPlugIn.py plugin...\n")
				mel.eval('loadPlugin "QuadRemesherPlugIn.py"')
				
			print ("Test ExoMesh import Mesh...\n")
			cmds.ImportExoMesh()
			'''
				
			# --- 1 - define folders and paths  ---
			isMacOSX = (platform.system()=="Darwin") or (platform.system()=="macosx")
			if isMacOSX :
				XRTempFolder = "/var/tmp/Exoside"
			else :
				XRTempFolder = os.path.join(tempfile.gettempdir(), "Exoside")
			#sys.stdout.write("TempFolder = "+ XRTempFolder + "\n")

			if not os.path.exists(XRTempFolder):
				os.makedirs(XRTempFolder)
			
			export_path = os.path.join(XRTempFolder, "QuadRemesher/Maya")
			export_path = unixifyPath(export_path)

			if not os.path.exists(export_path):
				os.makedirs(export_path)

			exportFilename = os.path.join(export_path, 'scene.fbx')
			retopoFilename = os.path.join(export_path, 'retopo.fbx')
			settingsFilename = os.path.join(export_path, 'RetopoSettings_Maya.txt')
			progressFilename = os.path.join(export_path, 'progress.txt')
			
			if isMacOSX :
				enginePath = script_folder+"/../QuadRemesher/xremesh"
			else:
				enginePath = script_folder+"/../QuadRemesher/xremesh.exe"

			# unixify path (sinon probleme sur command mel...)		
			exportFilename = unixifyPath(exportFilename)
			retopoFilename = unixifyPath(retopoFilename)
			settingsFilename = unixifyPath(settingsFilename)
			enginePath = unixifyPath(enginePath)
			
			#sys.stdout.write("exportFilename: " + exportFilename + "\n")
			#sys.stdout.write("retopoFilename: " + retopoFilename + "\n")
			#sys.stdout.write("settingsFilename: " + settingsFilename + "\n")
			#sys.stdout.write("enginePath: " + enginePath + "\n")

			# get user options:		
			_TargetQuadCount = self.targetQuadCountSpinBox.value()
			_CurvatureAdaptivness = self.curvatureAdaptivnessSpinBox.value()
			_AdaptQuadCount = self.adaptQuadCount.isChecked()
			_UseVertexColor = self.useVertexColor.isChecked()
			# OLD SYM: 
			# _Symmetry = self.symmetry.isChecked()
			_Symmetry_x = self.symmetry_x.isChecked()
			_Symmetry_y = self.symmetry_y.isChecked()
			_Symmetry_z = self.symmetry_z.isChecked()
			_UseMaterials = self.useMaterials.isChecked()
			_UseHardEdges = self.useHardEdges.isChecked()
			_UseIndexedNormals = self.useIndexedNormals.isChecked()
			_AutoDetectHardEdges = self.autoDetectHardEdges.isChecked()
			
			# save selected objects names:
			inputSelection = mel.eval('ls -sl')
			if (inputSelection==None) or (len(inputSelection)!=1):
				cmds.confirmDialog( title='QuadRemesher warning', message='You must select one and only one Mesh object!', button=['OK'])
				return
				
			# --- 2.1 - export mesh ----
			if True: # Use FBXExport (-s means selection only)
				# save FBX settings for restore
				saved_ExportHardEdges = mel.eval('FBXExportHardEdges -q')
				saved_ExportInputConnections = mel.eval('FBXExportInputConnections -q')
				saved_ExportScaleFactor = mel.eval('FBXExportScaleFactor -q')
				saved_ExportUpAxis = mel.eval('FBXExportUpAxis -q')
				saved_ExportSmoothingGroups = mel.eval('FBXExportSmoothingGroups -q')

				if mayaMajorVersion >= 2016:
					mel.eval('FBXExportFileVersion -v FBX201600')
				elif mayaMajorVersion >= 2014:
					mel.eval('FBXExportFileVersion -v FBX201400')
				else:
					mel.eval('FBXExportFileVersion -v FBX201200')
				#mel.eval('FBXExportFileVersion -v FBX201600')
				mel.eval('FBXExportGenerateLog -v false')
				mel.eval('FBXExportHardEdges -v false') # NB: This option allows to Duplicate vertices along HardEdges!!!!  (verified from my tests!!)
				mel.eval('FBXExportInputConnections -v false')
				mel.eval('FBXExportScaleFactor 1')
				mel.eval('FBXExportUpAxis y')  # needed to avoid axis swapping (needed for symmetry options)
				# NB: 'FBXExportSmoothingGroups'   NB: In the doc this option means: "Convert HardEdges flags to SmoothingGroups during export".  From My Test: if true it exports the HardEdge flags in 'SmoothingGroups' element as EdgeFlags, if False : doesn't export the hardEdge informations
				if _UseHardEdges:
					mel.eval('FBXExportSmoothingGroups -v true') 
				else:
					mel.eval('FBXExportSmoothingGroups -v false') 
				
				melCmd = 'FBXExport -f "%s" -s;' % exportFilename
				mel.eval(melCmd)
				
				# restore export options:
				mel.eval('FBXExportHardEdges -v '+str(saved_ExportHardEdges))
				mel.eval('FBXExportInputConnections -v '+str(saved_ExportInputConnections))
				mel.eval('FBXExportScaleFactor '+str(saved_ExportScaleFactor))
				mel.eval('FBXExportUpAxis '+str(saved_ExportUpAxis))
				mel.eval('FBXExportSmoothingGroups -v '+str(saved_ExportSmoothingGroups))
				
			else:
				melCmd = 'file -force -options "groups=1;ptgroups=1;materials=%d;smoothing=%d;normals=0" -typ "FBX export" -pr -es "%s";' % (int(_UseMaterials), int(_UseHardEdges), exportFilename)
				#sys.stdout.write("melCmd = " + melCmd + "\n")
				mel.eval(melCmd)
			
			# --- 2.2 - write remeshing settings ----
			# update persistent vars
			setOptionVarInt('QRtargetQuadCount', _TargetQuadCount)
			setOptionVarInt('QRcurvatureAdaptivness', _CurvatureAdaptivness)
			setOptionVarInt('QRadaptQuadCount', _AdaptQuadCount)
			setOptionVarInt('QRuseVertexColor', _UseVertexColor)
			# OLD SYM: setOptionVarInt('QRsymmetry', _Symmetry)
			setOptionVarInt('QRsymmetry_x', _Symmetry_x)
			setOptionVarInt('QRsymmetry_y', _Symmetry_y)
			setOptionVarInt('QRsymmetry_z', _Symmetry_z)
			setOptionVarInt('QRuseMaterials', _UseMaterials)
			setOptionVarInt('QRuseHardEdges', _UseHardEdges)
			setOptionVarInt('QRuseIndexedNormals', _UseIndexedNormals)
			setOptionVarInt('QRautoDetectHardEdges', _AutoDetectHardEdges)
			
			settings_file = open(settingsFilename, "w")
			settings_file.write('HostApp=Maya\n')
			settings_file.write('FileIn="%s"\n' % exportFilename)
			settings_file.write('FileOut="%s"\n' % retopoFilename)
			settings_file.write('ProgressFile="%s"\n' % progressFilename)
			
			settings_file.write("TargetQuadCount=%s\n" % _TargetQuadCount)
			settings_file.write("CurvatureAdaptivness=%s\n" % str(_CurvatureAdaptivness))
			settings_file.write("UseVertexColorMap=%d\n" % _UseVertexColor)
			settings_file.write("ExactQuadCount=%d\n" % (not _AdaptQuadCount))
			
			settings_file.write("UseMaterialIds=%d\n" % _UseMaterials)      
			# settings_file.write("UsePolygonGroups=%d\n" % UsePolygonParts)
			settings_file.write("UseHardEdgeFlags=%d\n" % _UseHardEdges)
			settings_file.write("UseIndexedNormals=%d\n" % _UseIndexedNormals)
			settings_file.write("AutoDetectHardEdges=%d\n" % _AutoDetectHardEdges)

			# 30 oct 2018: because I'm using 'merge' option in importer, I absolutly need to have a unique filename!!!
			inputMeshName = inputSelection[0]
			startIndexSearchRange = 0
			#sys.stdout.write("inputMeshName = %s\n " % inputMeshName)
			if inputMeshName.startswith("Retopo_"):
				inputMeshName = inputMeshName[7:]
				#sys.stdout.write("inputMeshName = '%s'  (remove Retopo_)\n " % inputMeshName)
			else:   # handle Prefix with number "Retopo72_"
				match = re.match("^Retopo(\d+)_(.*)", inputMeshName)
				if match:
					inputMeshName = match.group(2)
					startIndexSearchRange = int(match.group(1))
					#sys.stdout.write("inputMeshName = '%s'  (keep regexpr group1)  startIndexSearchRange=%d \n " % (inputMeshName, startIndexSearchRange))
			
			for namingNumber in range(startIndexSearchRange, startIndexSearchRange+1000):
				if namingNumber == 0:
					testName = "Retopo" + "_" + inputMeshName
				else:
					testName = "Retopo" + str(namingNumber) + "_" + inputMeshName
				#sys.stdout.write("testName = %s\n" % testName)
				if mel.eval('objExists %s' % testName) == False:
					settings_file.write("RetopoNodeName=%s\n" % testName)
					break
				
			''' OLD SYM:
			if _Symmetry:
				userSymOn = mel.eval('symmetricModelling -query -symmetry')
				if userSymOn == 0:
					_Symmetry = False
					#sys.stdout.write("Set Symmetry False!!!\n")
			if _Symmetry:
				symAxis = mel.eval('symmetricModelling -query -axis')
				symAbout = mel.eval('symmetricModelling -query -about')
				settings_file.write('SymAxis=%s\n' % symAxis) 
				if (symAbout == "world"):
					settings_file.write("SymLocal=0\n")
				else:
					settings_file.write("SymLocal=1\n")
			'''
			# new sym:
			symAxisText = ''
			if _Symmetry_x : symAxisText = symAxisText + 'X'
			if _Symmetry_y : symAxisText = symAxisText + 'Y'
			if _Symmetry_z : symAxisText = symAxisText + 'Z'
			if symAxisText != '':
				settings_file.write('SymAxis=%s\n' % symAxisText) 
				settings_file.write("SymLocal=1\n")
			
			settings_file.close()


			# --- 3 - run the remeshing engine ---
			try:
				if (os.path.isfile(retopoFilename)):
					os.remove(retopoFilename)
				if (os.path.isfile(progressFilename)):
					os.remove(progressFilename)
					
				# using subprocess
				#sys.stdout.write("Launch : path=" + enginePath + "\n")
				#sys.stdout.write("    settings_path=" + settingsFilename + "\n")
				remeshProc = subprocess.Popen([enginePath, "-s", settingsFilename])   #NB: Popen automatically add quotes around parameters when there are SPACES inside

			except Exception:
				import traceback
				sys.stdout.write("Execute remesher error: " + str(traceback.format_exc()) + "\n")
				
			# Wait for result:
			mel.eval('global string $gMainProgressBar') #initialize the progress bar
			mel.eval('progressBar -edit -beginProgress -isInterruptable true -status "Remeshing ..." -maxValue 100 $gMainProgressBar')

			Aborted = False
			SafetyCount=0
			ProgressValueFloat = 0
			ProgressText = ""
			sleepTime=0.1 # start with 0.1, updated after... check progress every 'sleepTime'
			
			#while not os.path.exists(retopoFilename):
			while True:

				time.sleep(sleepTime)   # time in seconds
				SafetyCount=SafetyCount+1
				
				# read progress file:
				progressLines=[]
				try:
					pf = open(progressFilename, "r")
					progressLines = pf.read().splitlines()
					pf.close()
				except Exception:
					if SafetyCount>2/sleepTime :   # after 2 seconds without progressFile..
						sys.stdout.write(' WARNING : no progressFile....')
					if SafetyCount>40/sleepTime :   # after 40 seconds without progressFile..
						break
				
				if len(progressLines)>=1:
					#sys.stdout.write(progressLines[0])
					try:
						ProgressValueFloat = float(progressLines[0])
					except Exception:
						sys.stdout.write(' error in progressbar...')
						
					if ProgressValueFloat != None:
						if (ProgressValueFloat < 0):
							if len(progressLines)>=2:
								ProgressText = progressLines[1]
							break
						# Succeded ?
						if ProgressValueFloat == 2:
							break

						newPBarValue = int( (99.0 * ProgressValueFloat + 1.0) * 10.0) / 10.0
						#myMelCmd = 'progressBar -edit -progress '+str(newPBarValue)+ ' $gMainProgressBar' # ca cree des warning...
						myMelCmd = 'progressBar -edit -progress %d $gMainProgressBar' % newPBarValue
						mel.eval(myMelCmd)

						canceled = mel.eval('progressBar -query -isCancelled $gMainProgressBar')
						if (canceled == True):
							Aborted = True
						
						# update sleepTime
						if SafetyCount >= 3 and ProgressValueFloat < 0.6:  # in middle of long process...check less often
							sleepTime = 0.4
						if ProgressValueFloat > 0.7 and SafetyCount < 10:  # approaching end of Progress... check more often
							sleepTime = 0.1
				
				# check process is running:
				if (remeshProc.poll() != None):
					ProgressValueFloat = -3    # this means that the remesher crashed
					ProgressText = "Remeshing Failed! (-3)"
					break
					
				if Aborted:
					break
			# end of while loop
		
			if Aborted:
				remeshProc.kill()

			mel.eval('progressBar -edit -endProgress $gMainProgressBar;')		 # kill the progress bar
			
			if ProgressValueFloat < 0:   # RemeshingFailed!
				#sys.stdout.write("ProgressValueFloat<0 : ProgressTest = '" + str(ProgressText) + "'\n")
				if (ProgressText != None and len(ProgressText)>0):
					cmds.confirmDialog( title='QuadRemesher', message=ProgressText, button=['OK'])
				return
			if Aborted:
				if (verboseDebug): sys.stdout.write("Remeshing ABORTED by user\n")
				return
				
				
			# --- 4 - import the retopo ---
			# The HUGE difference between FBXImport and 'file -import...' is that, FBXImport is NOT breaking the undos!!!
			# It's not perfect as the import itself is not undoable, but all the steps before the remeshing are undone at Ctrl-Z!
			# pour gerer ca proprement, il faudrait que je fasse une commande, et que je gere les methodes undo et redo moi meme .....
			# NB: For a good Import, the Import settings must be the default ones... (specially Group and namespace) ( don't know how to change them without using the 'file' MEL cmd (it break the undo))
			if (verboseDebug): sys.stdout.write("Importing Retopo....\n")
			if True:
				nodesListBeforeImport = mel.eval("ls")
				
				# save modified import options:
				saved_importMode = mel.eval('FBXImportMode -q')
				saved_generateLog = mel.eval('FBXImportGenerateLog -q')
				saved_importHardEdges = mel.eval('FBXImportHardEdges -q')
				saved_importUnlockNormals = mel.eval('FBXImportUnlockNormals -q')
				saved_importShapes = mel.eval('FBXImportShapes -q')
				saved_importScaleFactor = mel.eval('FBXImportScaleFactor -q')
				
				# set import options:
				#mel.eval('FBXImportMode -v "add"')
				mel.eval('FBXImportMode -v "merge"')   # this will 'merge' the potential folder, and 'add' the retopo mesh because the name has been changed
				mel.eval('FBXImportGenerateLog -v false')
				mel.eval('FBXImportHardEdges -v false') # means that Maya will merge points.... c'est l'equivalent de "Combine per-vertex Normals" de l'importer (UI)
				if (_UseHardEdges or _AutoDetectHardEdges or _UseIndexedNormals):
					mel.eval('FBXImportUnlockNormals -v true') # c'est l'equivalent de "Unlock Normals" de l'importer : IMPORTANT: ca permet de charger les HardEdges!!!
				else:
					mel.eval('FBXImportUnlockNormals -v false') # dans ce cas, pas de HardEdges a charger, il faut donc faire recalculer les normales a Maya -> need "Unlock Normals" = false
				
				mel.eval('FBXImportShapes -v true')
				# dans la doc, mais ne fonctionne pas... mel.eval('FBXImportScaleFactorEnable false;')
				mel.eval('FBXImportScaleFactor 1.0;')
				
				# import the retopo:
				myMelCmd = 'FBXImport -f "'+retopoFilename+'";'
				#sys.stdout.write('MyMelCmd = '+myMelCmd)
				mel.eval(myMelCmd)   
				
				# restore import options:
				mel.eval('FBXImportMode -v "'+str(saved_importMode)+'"')
				mel.eval('FBXImportGenerateLog -v '+str(saved_generateLog))
				mel.eval('FBXImportHardEdges -v '+str(saved_importHardEdges))
				mel.eval('FBXImportUnlockNormals -v '+str(saved_importUnlockNormals))
				mel.eval('FBXImportShapes -v '+str(saved_importShapes))
				mel.eval('FBXImportScaleFactor '+str(saved_importScaleFactor))
				
				# Select new one and hide the input mesh
				# NB: FBXImport does not returns the list of imported objects... just "Sucess"
				if (verboseDebug): sys.stdout.write("Select Retopo....\n")
				try:
					nodesListAfterImport = mel.eval("ls")
					diffSet = set(nodesListAfterImport) - set(nodesListBeforeImport)
					importedObjList = list(diffSet)
					
					retopoTransformNode = None
					retopoMeshNode = None
					for obj in importedObjList:
						if (mel.eval("objectType %s" % obj) == "transform"):
							retopoTransformNode = obj
						if (mel.eval("objectType %s" % obj) == "mesh"):
							retopoMeshNode = obj
						
					retopoNode = retopoTransformNode
					if retopoNode == None:
						retopoNode = retopoMeshNode
						
					if (verboseDebug):
						#sys.stdout.write("nodesListBeforeImport='"+str(nodesListBeforeImport)+"'\n")
						#sys.stdout.write("nodesListAfterImport='"+str(nodesListAfterImport)+"'\n")
						sys.stdout.write("importedObjList='"+str(importedObjList)+"'\n")
						sys.stdout.write("retopoNode='"+str(retopoNode)+"'\n")
				except Exception:
					sys.stdout.write('EXCEPTION: finding imported node...')

				if (verboseDebug): sys.stdout.write("Copy Attr....\n")
				try:
					# copy some attributes from SourceNode to RetopoNode
					# NB: copyAttr 'All' ne fonctionne pas... donc je les recopie a la main...
					if retopoNode != None:
						cmds.setAttr("%s.displayEdges" % str(retopoNode), cmds.getAttr("%s.displayEdges" % inputSelection[0]));
						#cmds.copyAttr('%s'%inputSelection[0], '%s'%str(retopoNode), inConnections=False, outConnections=False, values=True)
				except Exception:
					import traceback
					sys.stdout.write("EXCEPTION while copying attributes...: " + str(traceback.format_exc())+"\n")
					
				if (verboseDebug): sys.stdout.write("Hide input mesh....\n")
				try:
					# Hide SourceNode			
					mel.eval('hide "%s"' % inputSelection[0])
					
					# Select RetopoNode
					if retopoNode != None:
						myMelCmd = 'select -r "'+str(retopoNode)+'";'
						mel.eval(myMelCmd)
				except Exception:
					sys.stdout.write('EXCEPTION while hiding and selecting...')
				
			else:
				# using file command : https://download.autodesk.com/us/maya/2009help/Commands/file.html#flagreturnNewNodes
				mel.eval('FBXImportMode -v "add";')
				mel.eval('FBXImportGenerateLog -v false;')
				myMelCmd = 'file -import -type "FBX"  -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace "retopo" -options "fbx"  -pr  -returnNewNodes -importTimeRange "combine" "' + retopoFilename + '";'
				#sys.stdout.write('MyMelCmd = '+myMelCmd)
				importedObjects = mel.eval(myMelCmd)
				#sys.stdout.write('ImportedObj = '+str(importedObjects))

				myMelCmd = 'select -r "'+str(importedObjects[0])+'";'
				mel.eval(myMelCmd)

		except Exception:
			import traceback
			sys.stdout.write("Exception: in remeshButton_onClicked..\n")
			sys.stdout.write(str(traceback.format_exc()) + "\n")



	def getLicMgrPath(self):
		script_folder = os.path.dirname(os.path.realpath(__file__))
		isMacOSX = (platform.system()=="Darwin") or (platform.system()=="macosx")
		if isMacOSX :
			licenseManagerPath = script_folder+"/../QuadRemesher/xrLicenseManager.app/Contents/MacOS/xrLicenseManager"
		else:
			licenseManagerPath = script_folder+"/../QuadRemesher/xrLicenseManager.exe"
		licenseManagerPath = unixifyPath(licenseManagerPath)
		return licenseManagerPath
		

	def licenseManagerButton_onClicked(self): # ------------------------------------ LicenseManager ----------------------------
		try:
			licenseManagerPath = self.getLicMgrPath()
			subprocess.Popen(["%s" % licenseManagerPath, "-hostApp", "Maya"])
		except Exception:
			import traceback
			sys.stdout.write("Exception: in licenseManagerButton_onClicked..\n")
			sys.stdout.write(str(traceback.format_exc()) + "\n")

	def webDocButton_onClicked(self): # ------------------------------------ WebDoc buton click ----------------------------
		try:
			webbrowser.open('https://exoside.com/quadremesherdata/plugins_webdoc_link.php?App=Maya')
		except Exception:
			import traceback
			sys.stdout.write("Exception: in webDocButton_onClicked..\n")
			sys.stdout.write(str(traceback.format_exc()) + "\n")

		
	def newVerButton_onClicked(self): # ---------------------------------------------- News button click -------------------
		try:
			sys.stdout.write("1\n")
			if (self.newVerUrl != None) :
				sys.stdout.write("2\n")
				# webbrowser.open(self.newVerUrl)
				
				licenseManagerPath = self.getLicMgrPath()
				sys.stdout.write("3 " + str(licenseManagerPath) + "\n")
				
				subprocess.Popen(["%s" % licenseManagerPath, "-cn", "-hostApp", "Maya"])
		except Exception:
			import traceback
			sys.stdout.write("Exception: in newVerButton_onClicked..\n")
			sys.stdout.write(str(traceback.format_exc()) + "\n")

	def switch_language(self):
		if self.language == 'English':
			self.label1.setText("目标四边面数量")
			# self.groupBox1.setText("四边面大小设置 ...")
			self.label2.setText("自适应大小")
			self.adaptQuadCount.setText("自适应四边化数量")
			self.useVertexColor.setText("使用顶点色表示四边化强度")
			self.label3.setText("四边化强度(绘制)")
			# self.groupBox2.setText("循环边控制 ...")
			self.useMaterials.setText("使用材质")
			self.useHardEdges.setText("使用已存在的 硬边/软边")
			self.useIndexedNormals.setText("使用法线折痕")
			self.autoDetectHardEdges.setText("按角度检测硬边")
			# self.groupBox3.setText("杂项 :")
			self.symLabel.setText("对称 : ")
			self.languageButton.setText('语言')
			self.licManagerButton.setText('许可证管理器')
			self.webDocButton.setText('帮助')
			self.language = 'Chinese'
		else:
			self.label1.setText("Target Quad Count")
			# self.groupBox1.setText("Quads size settings ...")
			self.label2.setText("Adaptive Size")
			self.adaptQuadCount.setText("Adaptive Quad Count")
			self.useVertexColor.setText("Use Vertex Colors for Quads Density")
			self.label3.setText("Quads Density (paint)")
			# self.groupBox2.setText("Edge Loops Control ...")
			self.useMaterials.setText("Use Materials")
			self.useHardEdges.setText("Use existing Harden/Soften edges")
			self.useIndexedNormals.setText("Use Normals Creasing")
			self.autoDetectHardEdges.setText("Detect Hard-Edges by angle")
			# self.groupBox3.setText("Misc ...")
			self.symLabel.setText("Symmetry : ")
			self.languageButton.setText('language ')
			self.licManagerButton.setText('License Manager')
			self.webDocButton.setText('Web Doc')
			self.language = 'English'


class QuadRemesher:

	def __init__(self):
		# get parent pointer
		#mayaMainWindowPtr = OpenMayaUI_1.MQtUtil.mainWindow()
		#if mayaMainWindowPtr is not None:
		#	self.mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QMainWindow)
		#else:
		#	print("Maya main window not found.")
		#	return
		
		if QuadRemesherWindow.theWindow == None:
			ui = QuadRemesherWindow()
			ui.show()
			QuadRemesherWindow.theWindow = ui
		else:
			if QuadRemesherWindow.theWindow.windowState() == Qt.WindowMinimized:
				QuadRemesherWindow.theWindow.setWindowState(Qt.WindowNoState)
				QuadRemesherWindow.theWindow.activateWindow()
			QuadRemesherWindow.theWindow.show()


