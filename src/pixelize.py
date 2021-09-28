import PIL
import argparse
from time import time
from PIL import Image, ImageFilter
from functools import partial
from itertools import repeat
import numpy as np
import concurrent.futures

filename = 'test10'
extension = '.jpg'
imagePath = '../assets/' + filename + extension
savePath = '../assets/edits/' + filename + 'pixelize' + extension

chunkSize = 100

def readImage(imagePath):
    try:
        image = Image.open(imagePath)
        return image
    except Exception as e:
        print(e)


def convertImageToArray(image):
    return np.array(image)


def convertArrayToImage(array):
    return Image.fromarray(array)

# probably a cube of colors
def helperFunction(pixelChunk):
    return np.full((np.size(pixelChunk,0),np.size(pixelChunk,1),np.size(pixelChunk,2)),np.mean(np.mean(pixelChunk, axis=0), axis=0))

def printSizes(box):
    print(np.size(box,0), np.size(box,1), np.size(box,2))

def pixelizePhoto(imageArray):
    rowSize = len(imageArray)
    columnSize = len(imageArray[0])
    for rowCount in range(1, rowSize,chunkSize):
        for columnCount in range(1, columnSize, chunkSize):
            try:
                imageArray[rowCount-1:rowCount+(chunkSize-1),columnCount-1:columnCount+(chunkSize-1)] = helperFunction(imageArray[rowCount-1:rowCount+(chunkSize-1),columnCount-1:columnCount+(chunkSize-1)])
            except Exception as e:
                print(e)
                   
                   
    
    return imageArray

if __name__ == '__main__':
    # read in image
    image = readImage(imagePath)
    imageArray = convertImageToArray(image)
    start = time()
    # do the processing
    imageArray = pixelizePhoto(imageArray)
    print('time elapsed: ', time() - start)
    # convert the data back to an image
    image = convertArrayToImage(imageArray)
    image.show()
    # image.save(savePath)
    
