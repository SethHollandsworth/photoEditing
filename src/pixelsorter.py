import PIL
import argparse
from PIL import Image, ImageFilter
from functools import partial
from itertools import repeat
import numpy as np
import concurrent.futures

filename = 'test10'
extension = '.jpg'
imagePath = '../assets/' + filename + extension
savePath = '../assets/edits/' + filename + '6' + extension

# define thresholds for light and dark
darkThreshold = 10
lightThreshold = 235
# true if sorting should be vertical
vertical = False


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


# Function sorts a single pixel at a time so (r,g,b) will make blue the highest value
# INPUTS: imageArray - numpy array of picture
#         redDominant - boolean if you want it to be red-dominant instead of blue dominant
def sortSinglePixel(imageArray, redDominant):
    for i in range(len(imageArray)):
        for j in range(len(imageArray[i])):
            imageArray[i][j] = sorted(imageArray[i][j], reverse=redDominant)
    return imageArray


def sortHelper(array):
    return sum(array)


def lightness(pixel):
    return sum(pixel)/3


def getFirstNotBlackX(array):
    return np.argmax(array > darkThreshold)


def getNextBlackX(array, startIdx):
    out = np.argmax(array[startIdx:] < darkThreshold) + startIdx
    if out == startIdx:
        return len(array) - 1
    return out - 1


def getFirstNotWhiteX(array):
    position = 0
    while lightness(array[position]) > lightThreshold:
        position += 1
        if position >= len(array):
            return 0
    return position


def getNextWhiteX(array):
    position = 0
    while lightness(array[position]) < lightThreshold:
        position += 1
        if position >= len(array):
            return len(array)-1
    return -1

# def sortPhoto(imageArray):
#     # rows = [i for i in range(len(imageArray))]
#     for i in range(len(imageArray)):
#         startIdx = getFirstNotBlackX(imageArray[i])
#         endIdx = getNextBlackX(imageArray[i])
#         imageArray[i][startIdx:endIdx] = sorted(
#             imageArray[i][startIdx:endIdx], key=sortHelper)
#     return imageArray


# def sortPhoto(imageArray):
#     rows = range(len(imageArray))
#     with Pool(8) as p:
#         p.map(
#             partial(workerFunction, imageArray=imageArray), rows)
#     return imageArray
def sortPhoto(imageArray):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(workerFunction, imageArray)
    return imageArray


def workerFunction(row):
    startIdx = getFirstNotBlackX(row)
    endIdx = getNextBlackX(row, startIdx)
    row[startIdx:endIdx] = sorted(
        row[startIdx:endIdx], key=sortHelper)


def getEdges(image):
    # edge detection required greyscale image
    grey = image.convert('L')
    # get the edges
    edges = image.filter(ImageFilter.FIND_EDGES)
    return edges


# if __name__ == '__main__':
#     # parser = argparse.ArgumentParser(
#     #     description='pixelsort an image and save the output')
#     # parser.add_argument('-o', action='store', dest='savePath',
#     #                     help='the output path of saved photo')
#     # parser.add_argument('-m', action='store', dest='mode',
#     #                     help='the mode of the pixel sorting:\n0 - default, sort after black pixels\n1 - sort after white pixels')
#     main()
if __name__ == '__main__':
    image = readImage(imagePath)
    count = 0
    # a little turny turn
    if vertical:
        image = image.rotate(90, expand=True)
    imageArray = convertImageToArray(image)
    imageArray = sortPhoto(imageArray)
    image = convertArrayToImage(imageArray)
    # and stick the landing
    if vertical:
        image = image.rotate(270, expand=True)
    # image.show()
    image.save(savePath)
