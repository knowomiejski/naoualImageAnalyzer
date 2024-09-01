from manager.imageAnalyzer import ImageAnalyzer
from gui.imageAnalyzerGui import ImageAnalyzerGui

def main():
    imageAnalyzer = ImageAnalyzer()
    imageAnalyzerGui = ImageAnalyzerGui(imageAnalyzer)

if __name__ == "__main__":
    main()