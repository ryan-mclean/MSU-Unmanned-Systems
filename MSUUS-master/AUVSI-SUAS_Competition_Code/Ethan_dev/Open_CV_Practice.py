#code mostly from https://realpython.com/python-opencv-color-spaces/
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
"""
sexton_tshirt = cv2.imread('Sexton_Tshirt_logo.PNG')
sexton_banner = cv2.imread('Sexton_banner_logo.PNG')
sexton_banner_rgb = cv2.cvtColor(sexton_banner, cv2.COLOR_BGR2RGB)
sexton_tshirt_rgb = cv2.cvtColor(sexton_tshirt, cv2.COLOR_BGR2RGB)

red_upper = np.array([256, 256, 256])
red_lower = np.array([50, 0, 0])

mask = cv2.inRange(sexton_banner_rgb, red_lower, red_upper)
print(sexton_banner_rgb[360][1600])
print(sexton_banner_rgb[36][1533])
print(mask[36][1533])
for i in range(len(mask)):
    for j in range(len(mask[i])):
        if mask[i][j] == 0:
            sexton_banner[i][j] = [255, 0, 0]
        else:
            sexton_banner[i][j] = [0, 0, 0]

mask = cv2.inRange(sexton_tshirt_rgb, red_lower, red_upper)
print(sexton_tshirt_rgb[5][1335])
print(sexton_tshirt_rgb[558][1101])
print(mask[558][1101])
for i in range(len(mask)):
    for j in range(len(mask[i])):
        if mask[i][j] == 0:
            sexton_tshirt[i][j] = [255, 0, 0]
        else:
            sexton_tshirt[i][j] = [0, 0, 0]

Cf = cv2.imread('clifford football.jpg')
Grass = cv2.imread('Grass1.png',0)
#plt.imshow(Cf)
#plt.show()
Cf_rgb = cv2.cvtColor(Cf, cv2.COLOR_BGR2RGB)
#plt.imshow(Cf_rgb)
#plt.show()
Cf_hsv = cv2.cvtColor(Cf, cv2.COLOR_BGR2HSV)
#plt.imshow(Cf_hsv)
#plt.show()
Cf_gray = cv2.cvtColor(Cf, cv2.COLOR_BGR2GRAY)
#plt.imshow(Cf_gray)
#plt.show()
"""
"""
(thresh, im_bw) = cv2.threshold(Cf_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#plt.imshow(im_bw, cmap='Greys_r')
#plt.show()
light_red = (190, 255, 255)
dark_red = (160, 160, 150)
light_green = (100, 250, 170)
dark_green = (50, 150, 100)
light_blue = (200, 255, 100)
dark_blue = (100, 150, 40)
#lo_square = np.full((10, 10, 3), light_green, dtype=np.uint8) / 255.0
#do_square = np.full((10, 10, 3), dark_green, dtype=np.uint8) / 255.0
#plt.subplot(1, 2, 1)
#plt.imshow(hsv_to_rgb(do_square))
#plt.subplot(1, 2, 2)
#plt.imshow(hsv_to_rgb(lo_square))
#plt.show()
mask = cv2.inRange(Cf_hsv, dark_red, light_red)
result = cv2.bitwise_and(Cf_rgb, Cf_rgb, mask=mask)
plt.subplot(1, 2, 1)
plt.imshow(mask, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()
"""
"""
# Read image
im = cv2.imread("clifford football.jpg", cv2.IMREAD_GRAYSCALE)
# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200
# Filter by Area.
params.filterByArea = True
params.minArea = 950
# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.1
# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.87
# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0.01
# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
else:
    detector = cv2.SimpleBlobDetector_create(params)
# Detect blobs.
keypoints = detector.detect(im)
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# Show blobs
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
"""
#test images
#img = cv2.imread('image0 copy.jpg')
#img = cv2.imread('smiley_grass_black.jpg')
#img = cv2.imread('smiley_grass_white.jpg')
#img = cv2.imread('smiley_grass.jpg')
#img = cv2.imread('Grass_big_pentagon.jpg')
img = cv2.imread('Grass_pentagon.jpg')
#img = cv2.imread('Grass1_2_red_square.jpg')
#img = cv2.imread('InkedGrass1.jpg')
#img = cv2.imread('test copy.jpeg')
#img = cv2.imread('test_image copy.png')
#img = cv2.imread('Grass_tiles.PNG')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

def crop_img(img,indx,done=False):
    if done is False:
        plt.imshow(img)
        plt.show()
        #sets the background of the image to black
        mask = np.zeros(img.shape[:2],np.uint8)
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        rect = (50,50,450,290)
        cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        img = img*mask2[:,:,np.newaxis]
        plt.imshow(img)
        #plt.show()

    #picks out a specific object in the image and crops out everything but that
    #code from opencv's website on watershed
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0
    markers = cv2.watershed(img, markers)
    img[markers == -1] = [255, 255, 255]
    loc = []
    plt.imshow(img)
    plt.show()

    #performs the cropping of the image
    for i in range(len(markers)):
        for j in range(len(markers[i])):
            if markers[i][j] == 1:
                loc.append((i, j))
    if len(loc)>1:
        loc.pop(0)
        x = []
        for i in range(len(loc)):
            x.append(loc[i][0])
        y = []
        for i in range(len(loc)):
            y.append(loc[i][1])
        minx = np.min(x)-3
        miny = np.min(y)-3
        maxx = np.max(x)+3
        maxy = np.max(y)+3
        img[markers == -1] = [0, 0, 0]
        roi = img[minx:maxx, miny:maxy]
        #roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        plt.imshow(roi)
        plt.show()
"""
    #splits image to look for more objects
    i = 0
    j = 0
    x = x-minx
    y = y-miny
    xmin2 = np.min(x)
    ymin2 = np.min(y)
    xmax2 = xmin2
    ymax2 = ymin2
    while (x[i]-x[i+1]) < 4 and i < len(x)-2:
        xmax2 = x[i]
        i += 1
    xmin2 = minx

    while (y[j]-y[j+1]) < 4 and j < len(y)-2:
        ymax2 = y[j]
        j += 1
    ymin2 = miny
    print(y[j])
    print(x[i])
    print(xmin2)
    print(xmax2)
    print(ymin2)
    print(ymax2)
    img1 = roi[minx:xmax2, miny:ymax2]
    cv2.imwrite("output1.jpg",img1)
    plt.imshow(img1)
    plt.show()
    k = xmin2
    l = ymin2
    #print(len(roi_rgb[0][:]))
    #print(len(roi_rgb[:][0]))
    while k < xmax2:
        while l < ymax2:
            #print(k,l)
            roi[k,l] = [0,0,0]
            l += 1
        l = ymin2
        k += 1
    crop_img(roi,0,True)
    """
"""
    i = 0
    j = 0
    img_list = []
    if len(loc) < 1 or np.min(x) < 4 or np.min(y) < 4:
        return img_list
    print(x)
    print(y)
    while i < len(x)-1 and j < len(y)-1:
        if abs(x[i]-x[i+1]) > 3 or abs(y[i]-y[i+1]) > 3:
            roi_rgb_1 = roi_rgb[0:int((x[i]+x[i+1])/2)+3, 0:int((y[i]+y[i+1])/2)+3]
            roi_rgb = roi_rgb[int((x[i]+x[i+1])/2)+3:maxx, int((y[i]+y[i+1])/2)+3:maxy]
            name1 = "roi_rgb_"+str(indx)+".jpg"
            indx += 1
            name2 = "roi_rgb_"+str(indx)+".jpg"
            indx += 1
            cv2.imwrite(name1,roi_rgb)
            cv2.imwrite(name2,roi_rgb_1)
            img_list.append(roi_rgb)
            img_list.append(roi_rgb_1)
            break
        i += 1
        j += 1
    print(roi_rgb.shape)
    print(roi_rgb_1.shape)
    plt.subplot(1, 2, 1)
    plt.imshow(roi_rgb)
    plt.subplot(1, 2, 2)
    plt.imshow(roi_rgb_1)
    plt.show()
    img_list_1 = crop_img(cv2.imread(name1),indx, True)
    img_list_2 = crop_img(cv2.imread(name2),indx, True)
    img_list.append(img_list_1)
    print(img_list)
    img_list.append(img_list_2)
    print(img_list)
    return img_list
    """



list_img = np.array(crop_img(img,0))

#color identification:
"""
red = roi_rgb[:,:,2]
print(red.shape)
print(red[100][100])
print(red[50][50])
red_color_x = []
red_color_y = []
for i in range(red[0]):
    for k in i:
        if i[k]>0:
            red_color_x.append(i)
            red_color_y.append(i)
print(red_color_x)
print(red_color_y)
plt.imshow(red)
plt.show()
"""
"""
red_upper = np.array([180,255,255])
red_lower = np.array([100,150,70])
roi_hsv = cv2.cvtColor(roi_rgb, cv2.COLOR_RGB2HSV)
mask = cv2.inRange(roi_hsv, red_lower, red_upper)
result = cv2.bitwise_and(roi_rgb, roi_rgb, mask=mask)
plt.subplot(1, 2, 1)
plt.imshow(mask, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()
blue_upper = np.array([255,255,180])
blue_lower = np.array([70,150,100])
roi_hsv = cv2.cvtColor(roi_rgb, cv2.COLOR_RGB2HSV)
mask = cv2.inRange(roi_hsv, red_lower, red_upper)
result = cv2.bitwise_and(roi_rgb, roi_rgb, mask=mask)
plt.subplot(1, 2, 1)
plt.imshow(mask, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()
"""

#shape detection
"""
gray = cv2.cvtColor(roi_rgb, cv2.COLOR_BGR2GRAY)


ret,thresh = cv2.threshold(gray,127,255,1)

contours,h = cv2.findContours(thresh,1,2)
#print(contours)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    print(approx)
    if len(approx)==5:
        print("pentagon")
        cv2.drawContours(roi_rgb,[cnt],0,255,-1)
    elif len(approx)==3:
        print("triangle")
        cv2.drawContours(roi_rgb,[cnt],0,(0,255,0),-1)
    elif len(approx)==4:
        print("square")
        #cv2.drawContours(roi_rgb,[cnt],0,(0,0,255),-1)
    elif len(approx) == 9:
        print("half-circle")
        cv2.drawContours(roi_rgb,[cnt],0,(255,255,0),-1)
    elif len(approx) > 15:
        print("circle")
        cv2.drawContours(roi_rgb,[cnt],0,(0,255,255),-1)
plt.subplot(1, 2, 1)
plt.imshow(roi_rgb)
plt.subplot(1, 2, 2)
roi_rgb = roi_rgb[60:80,70:90]
plt.imshow(roi_rgb)
plt.show()
"""