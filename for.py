from PIL import Image, ImageDraw
from enum import Enum
import random, time, subprocess
 
#metadata for the images
width = 300
height = 300
 
frames = input("How many frames would you like the video to be: ")
frames = int(frames)
 
 
print()
 
#initialize our arrays
forestGrid = []
newForestGrid = []
 
 #Enums are slower than ints?
'''
class Colour(Enum):
    0 = 'empty'
    1 = 'green'
    2 = 'red'
            '''
#Colours
# 0 : Empty
# 1 : Green
# 2 : Red
 
#populate the arrays
for x in range(width):
    forestGrid.append([])
    for y in range(height):
        if random.randrange(2) == 0:
            forestGrid[x].append(1)
        else:
            forestGrid[x].append(0)
 
#timer for processing speed
startTime = time.time()
 
#the main loop
for f in range(int(frames)):
 
    #initialize our new image object
    img = Image.new('RGB', (width, height))
    pixel = img.load()
 
    #update grid
    for x in range(width):
        for y in range(height):
           
            newForestGrid = forestGrid
 
            if forestGrid[x][y] == 1:
                #set on fire
                if random.random() < 0.00000033:
                    newForestGrid[x][y] = 2
 
            elif forestGrid[x][y] == 0:
                #grow a tree
                if random.random() < 0.002:
                    newForestGrid[x][y] = 1
 
            elif forestGrid[x][y] == 2:
                #tree burns away
                if random.random() < 0.1:
                    newForestGrid[x][y] = 0
                #the fire spreads out
                else:
                    for dx in range(-1,2):
                        for dy in range(-1,2):
                            if x + dx >= 0 & x + dx > width - 1 & x + dx < width + 1 & y + dy >= 0 & y + dy > height - 1 & y + dy < height + 1:
                                if (forestGrid[x + dx][y + dy] == 1):
                                    newForestGrid[x + dx][y + dy] = 2
 
            #draw point for image                          
            if forestGrid[x][y] == 1:
                pixel[x, y] = (0, 204, 0)
            elif forestGrid[x][y] == 0:
                pixel[x, y] = (153, 76, 0)
            else:
                pixel[x, y] = (244, 66, 66)  
 
    #save it
    img.save("img/"+str(f)+".png")
 
    percentageFrames = str(round((f+1)/frames * 100, 2))
    elapsedTime = time.time() - startTime
    fps = round((f+1)/elapsedTime, 2)
    eta = str(round((frames - (f + 1)) / fps, 2))
 
    print(str(f+1)+"/" + str(frames) + " | " + percentageFrames +"%"+" | FPS: " + str(fps) + " | ETA: " + eta, end='\r')
 
    #delete objects
    del img
 
 
#make a video
videoSettings = "ffmpeg -r 30 -f image2 -s 1280x720 -i "
videoPath =  "img/%d.png"
videoCodex = " -vcodec libx264 -crf 25 -pix_fmt yuv420p "
videoOutput = "vid/out.mp4 -y"
subprocess.Popen(videoSettings+videoPath+videoCodex+videoOutput)