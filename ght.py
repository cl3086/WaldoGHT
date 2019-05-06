import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import sobel

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
            if accumulator[i][j] >= max:
                coordinates = (j, i)
                max = accumulator[i][j]
    return coordinates

def getEdges(path, minThreshold, maxThreshold):
    image = cv2.imread(path)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurredImage = cv2.GaussianBlur(grayscale, (3, 3), 0)
    return cv2.Canny(blurredImage, minThreshold, maxThreshold)

def houghTransform(image, imageEdges, referenceEdges, origin):
    RTable = createRTable(referenceEdges, origin)
    accumulator = createAccumulatorArray(imageEdges, RTable)
    length, width = imageEdges.shape
    coordinates = getMaxVote(accumulator, length, width)

    print(coordinates)
    length, width = referenceEdges.shape
    topLeft = (int(coordinates[0] - width/2), int(coordinates[1] + length/2))
    bottomRight = (int(coordinates[0] + width/2), int(coordinates[1] - length/2))
    img = cv2.rectangle(image, topLeft, bottomRight, (0,255,0), 3)
    cv2.imshow("Where's Waldo", img)

def main():
    image1 = cv2.imread("waldo1.jpg")
    referenceEdges1 = getEdges("referenceImage1.jpg", 150, 200)
    edges1 = getEdges("waldo1.jpg", 150, 200)
    image1Origin = (16,18)
    houghTransform(image1, edges1, referenceEdges1, image1Origin)

    # image2 = cv2.imread("waldo2.jpg")
    # referenceEdges2 = getEdges("referenceImage2.jpg", 200, 200)
    # edges2 = getEdges("waldo2.jpg", 100, 200)
    # cv2.imshow("test", referenceEdges2)
    # cv2.imshow("test2", edges2)
    # image2Origin = (31, 54)
    # houghTransform(image2, edges2, referenceEdges2, image2Origin)

    # image3 = cv2.imread("waldo3.jpg")
    # referenceEdges3 = getEdges("referenceImage3.jpg", 175, 300)
    # edges3 = getEdges("waldo3.jpg", 150, 200)
    # cv2.imshow("test", referenceEdges3)
    # cv2.imshow("test2", edges3)
    # image3Origin = (85, 85)
    # houghTransform(image3, edges3, referenceEdges3, image3Origin)

    # image4 = cv2.imread("waldo4.jpg")
    # referenceEdges4 = getEdges("referenceImage4.jpg", 100, 200)
    # edges4 = getEdges("waldo4.jpg", 150, 300)
    # image4Origin = (53, 78)
    # cv2.imshow("test", referenceEdges4)
    # cv2.imshow("test2", edges4)
    # houghTransform(image4, edges4, referenceEdges4, image4Origin)

    cv2.waitKey(0)

if __name__ == "__main__":
    main()
