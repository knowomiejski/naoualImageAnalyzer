from tkinter import *
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askdirectory
import threading
from models.directory import Directory
from os import path
from os import listdir
from os import walk
from os import fsdecode

class ImageAnalyzerGui:
    files = ()

    def __init__(self, imageAnalyzer) -> None:
        self.imageAnalyzer = imageAnalyzer
        self.startTinker();

    def startTinker(self):
        root = Tk()
        root.title("Naoual image analyzer")
        root.geometry("1400x900+100+50")
        root.minsize(700, 500)

        self.savingToLabelText = StringVar()
        self.savingToLabelText.set("No output folder selected")

        self.optionsForBestSegmentationStrategy = [
            "S",
            "M",
            "T",
        ]

        self.optionsForBestSegmentationSeries = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8"
        ]
        self.createSections(root)
        self.populateFrames()


        self.directoriesWithSegmentedImages = []
        self.frameDirectoriesWithSegmentedImages = {}
        root.mainloop()

    def createSections(self, root):
        self.leftFrame = Frame(root, bg='#05021c')
        self.rightFrame = Frame(root)

        root.columnconfigure(0, weight=4, minsize=230)
        root.columnconfigure(1, weight=8, minsize=700)

        root.rowconfigure(0, weight=1, minsize=250)
        root.rowconfigure(1, weight=1, minsize=250)

        self.leftFrame.pack(expand=True, fill="both")

        self.rightFrame.columnconfigure(1, weight=1, pad=5, minsize=700)
        self.rightFrame.rowconfigure(0, weight=1, minsize=400)
        self.rightFrame.rowconfigure(1, weight=1, minsize=400)

        self.leftFrame.grid(row=0, rowspan=2, column=0, sticky="nesw")
        self.rightFrame.grid(row=0, rowspan=2, column=1, sticky="nesw")

        #====================================================================================
        #TOP RIGHT
        self.cziFilesFrameParent = Frame(self.rightFrame)

        #Canvas child of cziFilesFrameParent
        self.cziFilesCanvas = Canvas(self.cziFilesFrameParent, bg='#12021a', scrollregion=(0, 0, 1000, 1000), bd=0, highlightthickness=0)
        self.cziFilesCanvas.pack(side=LEFT, expand=True, fill=BOTH)

        #Scrollbar of cziFilesFrameParent
        self.cziFilesScrollbar = Scrollbar(self.cziFilesFrameParent, orient="vertical", command=self.cziFilesCanvas.yview)
        self.cziFilesScrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
        self.cziFilesCanvas.config(yscrollcommand=self.cziFilesScrollbar.set)

        self.cziFilesFrame = Frame(self.cziFilesCanvas, bg='#12021a')
        self.cziFilesCanvasWindow = self.cziFilesCanvas.create_window((0,0), window=self.cziFilesFrame, anchor=NW)
        self.cziFilesFrameParent.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.cziFilesFrame.bind("<Configure>", self.OnFrameConfigureCziFiles)
        self.cziFilesCanvas.bind('<Configure>', self.FrameWidthCziFiles)
        #====================================================================================

        #====================================================================================
        #TOP RIGHT
        self.directoryFilesFrameParent = Frame(self.rightFrame)

        #Canvas child of directoryFilesFrameParent
        self.directoryFilesCanvas = Canvas(self.directoryFilesFrameParent, bg='#504c6b', scrollregion=(0, 0, 1000, 1000), bd=0, highlightthickness=0)
        self.directoryFilesCanvas.pack(side=LEFT, expand=True, fill=BOTH)

        #Scrollbar of directoryFilesFrameParent
        self.directoryFilesScrollbar = Scrollbar(self.directoryFilesFrameParent, orient="vertical", command=self.directoryFilesCanvas.yview)
        self.directoryFilesScrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
        self.directoryFilesCanvas.config(yscrollcommand=self.directoryFilesScrollbar.set)

        self.directoryFilesFrame = Frame(self.directoryFilesCanvas, bg='#504c6b')
        self.directoryFilesCanvasWindow = self.directoryFilesCanvas.create_window((0,0), window=self.directoryFilesFrame, anchor=NW)
        self.directoryFilesFrameParent.grid(row=1, column=0, columnspan=2, sticky=NSEW)

        self.directoryFilesFrame.bind("<Configure>", self.OnFrameConfigureDirectoryFiles)
        self.directoryFilesCanvas.bind('<Configure>', self.FrameWidthDirectoryFiles)
        #====================================================================================

    def FrameWidthCziFiles(self, event):
        canvas_width = event.width
        self.cziFilesCanvas.itemconfig(self.cziFilesCanvasWindow, width = canvas_width)

    def OnFrameConfigureCziFiles(self, event):
        self.cziFilesCanvas.configure(scrollregion=self.cziFilesCanvas.bbox("all"))

    def FrameWidthDirectoryFiles(self, event):
        canvas_width = event.width
        self.directoryFilesCanvas.itemconfig(self.directoryFilesCanvasWindow, width = canvas_width)

    def OnFrameConfigureDirectoryFiles(self, event):
        self.directoryFilesCanvas.configure(scrollregion=self.directoryFilesCanvas.bbox("all"))

    def populateFrames(self):
        self.savingToLabel = Label(self.leftFrame, textvariable=self.savingToLabelText)
        self.savingToLabel.grid(row=0, column=0, padx=5, pady=5,  sticky=NSEW)

        selectOutputButton = Button(self.leftFrame, text="Select output location", command=self.openSelectOutPutDialog)
        selectOutputButton.grid(row=1, column=0, padx=5, pady=5,  sticky=NSEW)

        selectFileButton = Button(self.leftFrame, text="Select files", command=self.openFilesSelectionDialog)
        selectFileButton.grid(row=2, column=0, padx=5, pady=5,  sticky=NSEW)

        findOutputsButton = Button(self.leftFrame, text="Find existing outputs", command=self.findExistingOutputs)
        findOutputsButton.grid(row=3, column=0, padx=5, pady=5,  sticky=NSEW)

        splitButton = Button(self.leftFrame, text="Split into images", command=self.splitSelectedCZIToImageStacks)
        splitButton.grid(row=4, column=0, padx=5, pady=5,  sticky=NSEW)

        runSegmentationsButton = Button(self.leftFrame, text="Run Segmentation", command=self.runSegmentations)
        runSegmentationsButton.grid(row=5, column=0, padx=5, pady=5,  sticky=NSEW)

        runDiameterJButton = Button(self.leftFrame, text="Run DiameterJ on Best Segmentations", command=self.runDiameterJOnBestSegmentations)
        runDiameterJButton.grid(row=6, column=0, padx=5, pady=5,  sticky=NSEW)

        runSummariesToExcelButton = Button(self.leftFrame, text="Summary to Excel", command=self.runSummariesToExcel)
        runSummariesToExcelButton.grid(row=7, column=0, padx=5, pady=5,  sticky=NSEW)

    def testPopulateList(self):
        for i in range(100):
            selectFileLabel = Label(self.cziFilesFrame)
            selectFileLabel.columnconfigure(0, weight=12)
            selectFileLabel.grid(row= i, columnspan=12, padx=5, pady=5, sticky="nesw")
            label = Label(selectFileLabel, text="Test file " + str(i), bg='#b1eba4')
            label.pack(expand=True, fill="both")

        for i in range(100):
            selectFileLabel = Label(self.directoryFilesFrame)
            selectFileLabel.columnconfigure(0, weight=12)
            selectFileLabel.grid(row= i, columnspan=12, padx=5, pady=5, sticky="nesw")
            label = Label(selectFileLabel, text="Test dir " + str(i), bg='#ebe8a4')
            label.pack(expand=True, fill="both")



    def openTestImage(self):
        self.imageAnalyzer.testLoadImage()

    def findExistingOutputs(self):
        self.directoriesWithSegmentedImages = []
        for frameDir in self.frameDirectoriesWithSegmentedImages:
            self.frameDirectoriesWithSegmentedImages[frameDir].destroy()
        self.frameDirectoriesWithSegmentedImages = {}
        absolutePath = path.abspath(path.join(self.getOutputDir(), ""))
        for dir in listdir(absolutePath):
            joinedDir = path.join(absolutePath, dir)
            if path.isdir(joinedDir):
                firstFile = path.join(joinedDir, dir + "_0001.tif")
                print("joinedDir:", joinedDir)


                if path.exists(firstFile):
                    print("File exists: ", firstFile)
                    print("Directory has split images")
                    newDirectory = Directory(directoryPath=joinedDir)
                    self.directoriesWithSegmentedImages.append(newDirectory)
                else:
                    continue


                bestSegmentation = path.join(joinedDir ,"Best Segmentation")
                if path.exists(bestSegmentation):
                    print("bestSegmentation:", bestSegmentation)
                    firstBestSegmentationFile = ""
                    for bestSegmentationFile in listdir(path.join(bestSegmentation, "")):
                        bestSegmentationFileName = fsdecode(bestSegmentationFile)
                        if bestSegmentationFileName.endswith(".tif"):
                            print("bestSegmentationFileName: " + bestSegmentationFileName)
                            firstBestSegmentationFile = path.abspath(bestSegmentationFile)
                            for directoryWithSegmentedImages in self.directoriesWithSegmentedImages:
                                if directoryWithSegmentedImages.getDirectoryPath() == joinedDir:
                                    fullStrategy = firstBestSegmentationFile.split("_")[-1].split(".")[0]
                                    print("fullStrategy: " + fullStrategy)
                                    selectedStrategy = ""
                                    selectedSeries = ""
                                    for character in fullStrategy:
                                        if character.isalpha():
                                            selectedStrategy = selectedStrategy + character
                                        else:
                                            selectedSeries=selectedSeries + character
                                    print("selectedStrategy: " + selectedStrategy)
                                    print("selectedSeries: " + selectedSeries)

                                    directoryWithSegmentedImages.setSelectedStrategy(selectedStrategy)
                                    directoryWithSegmentedImages.setSelectedSeries(selectedSeries)
                                    break
                                else:
                                    continue
                            break
                        else:
                            continue

                if path.exists(bestSegmentation):
                    histogramsDir = path.join(bestSegmentation, "Histograms")
                    if path.exists(histogramsDir):
                        print("Histograms exists", histogramsDir)
                        print("Directory has ran diameterj analysis")
                        for directoryWithSegmentedImages in self.directoriesWithSegmentedImages:
                            if directoryWithSegmentedImages.getDirectoryPath() == joinedDir:
                                directoryWithSegmentedImages.setHasBeenSegmented(True)
                                directoryWithSegmentedImages.setHasBeenAnalyzed(True)
                                break
                    else:
                        for directoryWithSegmentedImages in self.directoriesWithSegmentedImages:
                            if directoryWithSegmentedImages.getDirectoryPath() == joinedDir:
                                directoryWithSegmentedImages.setHasBeenSegmented(True)
                                break

        self.renderSegmentedFolders()

    def getOutputDir(self):
        return path.join(self.outPutDirectory)

    def setOutputDir(self, outputDir):
        return path.join(self.outPutDirectory)

    def openFilesSelectionDialog(self):
        self.files = askopenfilenames()
        self.renderFilesList()

    def openSelectOutPutDialog(self):
        self.outPutDirectory = askdirectory()
        self.imageAnalyzer.setOutputDir(self.outPutDirectory)
        self.savingToLabelText.set("Output: " + self.outPutDirectory)
        print("outPutDirectory", self.outPutDirectory)

    def removeItemFileFromList(self, file):
        filesList = list(self.files)
        filesList.remove(file)
        self.files = tuple(filesList)
        self.frameFiles[file].destroy()
        print("self.frameFiles[file]", self.frameFiles[file])
        print("self.files",  self.files)

    def removeItemDirectoryToAnalyzeFromList(self, directory: Directory):
        directoriesList = list(self.directoriesWithSegmentedImages)
        print("directoriesList", directoriesList)
        for dir in directoriesList:
            if dir.getDirectoryPath() == directory.getDirectoryPath():
                print("dir", dir.getDirectoryPath())
                self.frameDirectoriesWithSegmentedImages[dir.getDirectoryPath()].destroy()
                directoriesList.remove(dir)

        print("self.directoriesWithSegmentedImages",  self.directoriesWithSegmentedImages)
        self.directoriesWithSegmentedImages = tuple(directoriesList)

    def renderSegmentedFolders(self):
        i = 0
        self.frameDirectoriesWithSegmentedImages = {}
        for directory in self.directoriesWithSegmentedImages:

            hasBeenAnalyzedStr = "idk"
            if directory.getHasBeenAnalyzed():
                hasBeenAnalyzedStr = "Yes"
            else:
                hasBeenAnalyzedStr = "No"

            hasBeenSegmentedStr = "idk"
            if directory.getHasBeenSegmented():
                hasBeenSegmentedStr = "Yes"
            else:
                hasBeenSegmentedStr  = "No"


            labelname = directory.getDirectoryPath() + "// Segmented?: " + hasBeenSegmentedStr + " // Analyzed?: " + hasBeenAnalyzedStr
            selectFileLabel = Frame(self.directoryFilesFrame, pady=2)
            selectFileLabel.grid(row=i, column=0, columnspan=9, sticky="we")
            imageName = Label(selectFileLabel, text=labelname, bg='#ebe8a4', width=90)
            imageName.grid(row=0, column=0, columnspan=9, sticky="we")

            button = Button(selectFileLabel, text="X", command= lambda directory=directory: self.removeItemDirectoryToAnalyzeFromList(directory), pady=0)
            button.grid(row=0, column=11, sticky="we")

            optionMenuS = OptionMenu(selectFileLabel, directory.selectedSeries, *self.optionsForBestSegmentationSeries)
            optionMenuS.grid(row=0, column=10, sticky="we")

            optionMenuS = OptionMenu(selectFileLabel, directory.selectedStrategy, *self.optionsForBestSegmentationStrategy)
            optionMenuS.grid(row=0, column=9, sticky="we")

            self.frameDirectoriesWithSegmentedImages[directory.getDirectoryPath()] = selectFileLabel
            i = i + 1

    def renderFilesList(self):
        i = 0
        self.frameFiles = {}
        for file in self.files:
            frameFile = Frame(self.cziFilesFrame, pady=2)
            frameFile.grid(row=i, column=0, columnspan=9, sticky="we")
            imageName = Label(frameFile, text=file, bg="#b1eba4", width=90)
            imageName.pack(side=LEFT, expand=True, fill=BOTH)
            # imageName.grid(row=0, column=0, columnspan=11, sticky=NSEW)
            button = Button(frameFile, text="X", command= lambda file=file: self.removeItemFileFromList(file), pady=0)
            button.pack(side=RIGHT, expand=False, fill=BOTH)
            # button.grid(row=0, column=11,  sticky=NSEW)
            self.frameFiles[file] = frameFile
            i = i + 1

    def runSummariesToExcel(self):
        for directory in self.directoriesWithSegmentedImages:
            self.imageAnalyzer.summariesToExcel(directory)

    def runDiameterJOnBestSegmentations(self):
        for directory in self.directoriesWithSegmentedImages:
            self.imageAnalyzer.runDiameterJOnBestSegmentation(directory)

    def runSegmentations(self):
        for directory in self.directoriesWithSegmentedImages:
            print("Dir from runSegmentationButton", directory)
            self.imageAnalyzer.runSegmentation(directory)

    def splitSelectedCZIToImageStacks(self):
        for file in self.files:
            self.imageAnalyzer.splitFile(file)
            newDirectory = Directory(directoryPath=path.join(self.getOutputDir(), str(file).split('/')[-1].split('.')[0]).replace(" ", ""))
            self.directoriesWithSegmentedImages.append(newDirectory)

        self.renderSegmentedFolders()
