# Dependencies: > pip3 install opencv-python numpy matplotlib

import os
import cv2
import numpy as np
import statistics
import matplotlib.pyplot as plt
from pathlib import Path
import time
import FileHandler

image_paths = list()

workingDirectory = os.path.dirname(os.path.realpath(__file__))

#Recurse through wallpapers, gathering paths to all wallpapers
for path in Path(workingDirectory).rglob('*.jpg'):
    image_paths.append(str(path))

for path in Path(workingDirectory).rglob('*.png'):
    image_paths.append(str(path))

#Create lists of light/dark images 
lightImages, darkImages = list(), list()
lightImagesPath, darkImagesPath = workingDirectory+"/lImages.txt", workingDirectory+"/dImages.txt"

#Scanned Images handler
scannedImagesList = list()
if FileHandler.file_exists(lightImagesPath):
    scannedImagesList += FileHandler.read_file(lightImagesPath)
else:
    print("No light images file")
if FileHandler.file_exists(darkImagesPath):
    scannedImagesList += FileHandler.read_file(darkImagesPath)
else:
    print("No dark images file")

for scanned in scannedImagesList:
    if len(scannedImagesList) < 10:
        print("removing item: ", scanned)
    image_paths.remove(scanned)

if len(scannedImagesList) >= 10:
    print("Removed ", len(scannedImagesList), " items from to-be-scanned list, leaving: ", len(image_paths), " items.")

#time total execution
total_start = time.time()

for path_num in range(1):
    #Analyze each image for pixel data
        #Encode path as string(for analysis) and utf(for digest)
    str_path = image_paths[path_num]
    utf_path = image_paths[path_num].encode('utf-8')

    #Designate image for analysis
    image = cv2.imread(str_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    white_color = 255*3

    pixel = list()
    pixels_total = 0
    brightness_total = 0
    for i in range(0,image.shape[0]):
        for j in range(0,image.shape[1]):
            for k in range(0, image.shape[2]):
                if k == 0:
                    pixel = list()
                pixel.append( image.item(i, j, k) )
            #print("Pixel is: ",pixel," ; brightness is: ",pixel_brightness)
            pixels_total += 1
            brightness_total += sum(pixel) / white_color
    avg_brightness = brightness_total / pixels_total

    #Convert image to data that can be analyzed
        # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = image.reshape((-1, 3))
        # convert to float
    pixel_values = np.float32(pixel_values)

        # define stopping criteria: 100 iterations or 0.2 Epsilon
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

    # Start timer
    print("Begin Clustering", end='\r')
    start = time.time()

        # number of clusters (K)
    k = 5
    _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # End Timer and display runtime of command
    end = time.time()
    print(k, " Clusters completed in: ",end - start, " seconds.")

        # convert back to 8 bit values
    centers = np.uint8(centers)

        # flatten the labels array
    labels = labels.flatten()

        # convert all pixels to the color of the centroids
    segmented_image = centers[labels.flatten()]

    segmented_image = segmented_image.reshape(image.shape)

    # Clean Clustered colors list to only show uniques, will still be 5 colors(theoretically)
    clustered_colors_list = list()
    for color in centers[labels.flatten()].tolist():
        if color not in clustered_colors_list:
            clustered_colors_list.append(color)

    # Generate brightness ratio for each clustered color
    brightness_ratio_list = list()
    for color in clustered_colors_list:
        this_sum = 0
        for RGBvalue in color:
            this_sum += RGBvalue
        brightness_ratio_list.append(this_sum/white_color)

    avg_clust_brightness = (sum(brightness_ratio_list)/k)

    print("The path is: ", utf_path)
    print("Average brightness of image: ", avg_brightness)
    print("Average brightness of clusters: ", avg_clust_brightness)
    print("\n")

    threshold = 0.46

    if avg_brightness >= threshold:
        lightImages.append(str_path)
    else:
        darkImages.append(str_path)
if len(lightImages):
    print("Light Image")
    FileHandler.write_to_file(lightImagesPath, lightImages)
else:
    print("Dark Image")
    FileHandler.write_to_file(darkImagesPath, darkImages)

total_end = time.time()
print("Time taken: ", total_end-total_start, " secs.")
# show the image
#plt.imshow(segmented_image)
#plt.show()

#print(image_paths[0])