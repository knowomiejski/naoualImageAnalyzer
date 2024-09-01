from tkinter import StringVar


class Directory:
    directoryPath = ""
    hasBeenSegmented=False
    hasBeenAnalyzed=False

    def __init__(self, directoryPath):
        self.directoryPath = directoryPath
        self.selectedStrategy: StringVar = StringVar()
        self.selectedStrategy.set("T")
        self.selectedSeries: StringVar = StringVar()
        self.selectedSeries.set("1")


    def setHasBeenAnalyzed(self, hasBeenAnalyzed):
        self.hasBeenAnalyzed = hasBeenAnalyzed

    def setHasBeenSegmented(self, hasBeenSegmented):
        self.hasBeenSegmented = hasBeenSegmented

    def getHasBeenSegmented(self):
        return self.hasBeenSegmented

    def setSelectedStrategy(self, strategy):
        self.selectedStrategy.set(strategy)

    def setSelectedSeries(self, series):
        self.selectedSeries.set(series)

    def getDirectoryPath(self):
        return self.directoryPath

    def getHasBeenAnalyzed(self):
        return self.hasBeenAnalyzed

    def getSelectedStrategy(self):
        return self.selectedStrategy.get()

    def getSelectedSeries(self):
        return self.selectedSeries.get()

    def getFullStrategy(self):
        return self.selectedStrategy.get() + self.selectedSeries.get()