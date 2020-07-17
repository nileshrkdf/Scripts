#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 11:47:35 2020

@author: n=Nilesh Malviya
"""

import os

# constant 
baseFolderPath = "/path/to/your/sourcecode"
fileName = baseFolderPath + "/FileNameWithPath.txt"
ImagesName = baseFolderPath + "/ImageList.txt"
unUsedImagesName = baseFolderPath + "/UnUsedImageList.txt"
directoryFolderNameToSkip = ['.git', 'ExternalFrameworks'
                             , 'DerivedData', 'Localization', 'Pods', 'Scripts']
# variable         
fileList = list()
imageList = list()
unUsedImageList = list()

# Method to fetch the source code files and image files
def fetchImageAndFileList(baseFolderPath):
    # loop through all the directory and subdirectory to find all the image files 
    for root, dirs, files in os.walk(baseFolderPath, topdown=True):
        
        # removing the directory which needs to be skiped 
        for directoryToRemove in directoryFolderNameToSkip:
            if directoryToRemove in dirs:
                dirs.remove(directoryToRemove)
        
        # loop through all the files to filter out the image files      
        for file in files:
            # unpacking the tuple
            file_name, file_extension = os.path.splitext(file)
            # Checking the file extensions
            if file_extension == '.png' or file_extension == '.PNG' or file_extension == '.jpg' or file_extension == '.jpeg':
                # spliting the file name with the file name, like image@2x.png or image@3x.png
                imageName = file_name.split('@')[0]
                # checking for duplicate image name, if already then dont add it
                if imageName not in imageList :
                    imageList.append(imageName)
                    # Adding line break for readability 
                    imageList.append("\n")
                    
            # Adding the file path in the file list list
            fileList.append(os.path.join(root, file))
            # Adding line break for readability 
            fileList.append("\n")       

# Method to scan the code and find out the unused image files
def gettingListOfUnusedImages(imageList):
    # loop through image list and check if the image is being used or not
    for image in imageList:
        # Skiping the new line 
        if image != "\n":
            imageUsed = False
            # looping through the list of files
            for fileName in fileList:
                # Skiping the new line 
                if fileName != "\n":
                    # Spliting the file with extension so that only selected file extension will be scanned
                    file_name, file_extension = os.path.splitext(fileName)
                    if file_extension == '.swift' or file_extension == '.storyboard' or file_extension == '.xib' or file_extension == '.m':
                        # Reading the file
                        file = open(fileName, "r") 
                        for line in file:
                            # Finding the image name in the row
                            if (line.find(image) != -1):
                                imageUsed = True
                                break
            if imageUsed == False:
                unUsedImageList.append(image)
                # Adding line break for readability 
                unUsedImageList.append("\n")
                

# fetching the image and file list
fetchImageAndFileList(baseFolderPath)
# fetching the unused image list
gettingListOfUnusedImages(imageList)


# FileManager class help to write the data in the file    
class FileManager:
    def writeFile(self, fileName, data, writeType):
        f = open(fileName, writeType)
        f.writelines(data)
        f.close()
        
# Writing the list into files
fileManager = FileManager()
fileManager.writeFile(fileName, fileList, "w")
fileManager.writeFile(ImagesName, imageList, "w")
fileManager.writeFile(unUsedImagesName, unUsedImageList, "w")  
#print(len(imageList)/2)
