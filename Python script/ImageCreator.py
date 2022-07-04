from math import floor, sqrt
import cv2
import os
import numpy as np


imgPath = input("Enter the path to the folder where you have the sample images stored: ") or r"C:\Users\Game-PC\Pictures\Input"

images = []
for filename in os.listdir(imgPath):
    img = cv2.imread(os.path.join(imgPath,filename))
    if img is not None:
       images.append(img)

imgPath = input("Now enter the path to the image you want to create: ")
size = int(input("Enter the resolution you want the images to be: "))
size2 = int(input("Enter how many pixels each image will take up: "))

imgLooks = cv2.imread(imgPath)
imgLooks = cv2.resize(imgLooks, (int(imgLooks.shape[1]/size2),int(imgLooks.shape[0]/size2)))
samples= []


print("Calculating average colors:")
for y in range(len(images)):
    
    #square off sample images
    if(len(images[y]) > len(images[y][0])):
        for i in range(floor((len(images[y]) - len(images[y][0]))/2)):
            
            images[y] = images[y][1:]
            images[y] = images[y][:len(images[y])-1]
        if len(images[y]) - len(images[y][0]) != 0:
            images[y] = images[y][1:]

    elif(len(images[y]) < len(images[y][0])):
        

        times = floor((len(images[y][0]) - len(images[y]))/2)
        
        tmp = []
        for i in range(len(images[y])):
            if len(images[y]) - 2*times != 0:
                tmp.append(images[y][i][times+1:times+1+len(images[y])])
            else:
                tmp.append(images[y][i][times:times+len(images[y])])

        images[y] = np.array(tmp)
    images[y] = cv2.resize(images[y], (size,size))
    #add the average color of the sample image to the samples
    samples.append([y,np.average(np.average(images[y], axis=0), axis=0)])
    print(str(round(y/len(images)*100,2)) + "%", end="\r")
    



newImage = []
checkImage = []
checkImage2 = [[]]
i= 0


for i in samples:
    checkImage2[0].append(i[1])

print("100%   ")
print("Creating image:")

for index in range(len(imgLooks)):
    
    columnobj = []
    cir = []
    for pixel in imgLooks[index]:
        smallDiff = 0
        smallestDiff =100000000
        for i in samples:
            diff = sqrt(pow(i[1][0]-pixel[0],2)+pow(i[1][1]-pixel[1],2)+pow(i[1][2]-pixel[2],2))
            if diff < smallestDiff:
                smallestDiff = diff
                smallDiff = i
        columnobj.append(smallDiff[0])
        cir.append(smallDiff[1])

    


    for i in range(size): 
        rowPixels = []
        a= True
        for j in columnobj:
            if a:
                a = False
                rowPixels = images[j][i]
            else:
                rowPixels = np.append(rowPixels ,images[j][i],axis=0)
        newImage.append(rowPixels)
    checkImage.append(cir)
    
    print(str(round(index/len(imgLooks)*100,2)) + "%     ", end="\r")
    


print("100%     ")




print("Saving image(this has no loading bar wait for the next message)")
cv2.imwrite("Mosaic.png", np.array(newImage))
cv2.imwrite("ChosenColors.png", np.array(checkImage))
cv2.imwrite("ScaledDownImage.png", np.array(imgLooks))
cv2.imwrite("AvalibleColors.png", np.array(checkImage2))
print("Done, look in the folder of this program for mosaic.jpg")

input("Press enter to close: ")
