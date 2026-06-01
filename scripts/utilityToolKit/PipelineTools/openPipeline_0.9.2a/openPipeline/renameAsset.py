def renameAsset(folderPath,newName,oldName=''):
	
	import os;
	from os.path import join;
		
	isTopLevel = 0
	
	error=''
	
	if (oldName==''): # the first call, top level
		isTopLevel = 1
		split = os.path.split(folderPath)
		oldName = os.path.basename(split[0])
		newDirPath = folderPath.replace(oldName,newName)
		if os.path.isdir(newDirPath):
			error+='An asset with this name already exists.'
		
		
	if (error==''):		
		for root, dirs, files in os.walk(folderPath):
			for file in files:
				print 'renaming '+file
				newFileName = file.replace(oldName,newName)
				os.rename(os.path.join(root,file),os.path.join(root,newFileName))
			for dir in dirs:
				print dir
				nextFolderPath = os.path.join(folderPath,dir)
				renameAsset(nextFolderPath,newName,oldName)
				print 'renaming '+dir
				newDirName = dir.replace(oldName,newName)
				os.rename(os.path.join(root,dir),os.path.join(root,newDirName))
		
		
		if (isTopLevel): # rename the top level
			newDirPath = folderPath.replace(oldName,newName)
			os.rename(folderPath,newDirPath)
			
	else:
		print error
			