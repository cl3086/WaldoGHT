import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import sobel

referenceImage = cv2.imread("referenceimage1.jpg")
grayscale = cv2.cvtColor(referenceImage, cv2.COLOR_BGR2GRAY)
blurredImage = cv2.GaussianBlur(grayscale, (3, 3), 0)
referenceEdges = cv2.Canny(blurredImage, 10, 200)


image = cv2.imread("waldo1.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurredImage = cv2.GaussianBlur(gray, (3, 3), 0)
edges = cv2.Canny(blurredImage, 10, 200)


# show the images
# cv2.imshow("Original", image)
# cv2.imshow("Edges", edges)
# cv2.imshow("Reference Image", referenceEdges)
# cv2.imwrite("test.jpg", edges)
# cv2.imwrite("referenceEdges.jpg", referenceEdges)
# cv2.waitKey(0)

imageOrigin = (16,18)

def createRTable(referenceEdges, imageOrigin):
    dx = sobel(referenceEdges, axis=0)
    dy = sobel(referenceEdges, axis=1)
    phis = np.arctan2(dy,dx) * 180 / np.pi

    length, width = referenceEdges.shape
    RTable = {}

    for i in range(length):
        for j in range(width):
            if referenceEdges[i][j]:
                if phis[i,j] not in RTable:
                    RTable[phis[i,j]] = []
                RTable[phis[i,j]].append((imageOrigin[0] - i, imageOrigin[1] - j))
    return RTable

def createAccumulatorArray(imageEdges, RTable):
    length, width = imageEdges.shape
    accumulator = np.zeros((length, width))

    dx = sobel(imageEdges, axis=0)
    dy = sobel(imageEdges, axis=1)
    phis = np.arctan2(dy,dx) * 180 / np.pi

    for i in range(length):
        for j in range(width):
            if imageEdges[i][j] and phis[i,j] in RTable:
                for vector in RTable[phis[i,j]]:
                    if i + vector[0] < length and j + vector[1] < width:
                        accumulator[i + vector[0], j + vector[1]] += 1

    return accumulator

def getMaxVote(accumulator, length, width):
    max = -1
    coordinates = (-1,-1)
    for i in range(length):
        for j in range(width):
            if accumulator[i][j] > max:
                coordinates = (i, j)
                max = accumulator[i][j]
    return coordinates

RTable = createRTable(referenceEdges, imageOrigin)
accumulator = createAccumulatorArray(edges, RTable)
length, width = edges.shape
coordinates = getMaxVote(accumulator, length, width)
print(coordinates)

topLeft = (int(coordinates[1] - imageOrigin[0]), int(coordinates[0] + imageOrigin[1]))
bottomRight = (int(coordinates[1] + imageOrigin[0]), int(coordinates[0] - imageOrigin[1]))
print(topLeft, bottomRight)
img = cv2.rectangle(image, topLeft, bottomRight, (0,255,0), 3)
cv2.imshow("Image", img)
cv2.waitKey(0)
