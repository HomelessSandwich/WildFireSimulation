from PIL import Image, ImageDraw
import time, subprocess
from random import random, randrange

#metadata for the images
width = 300
height = 300

frames = input("How many frames would you like the video to be: ")
frames = int(frames)
 
print()

#initialize our arrays
soilGrid = []
treeGrid = []
fireGrid = []

soilGridIndex = -1
treeGridIndex = -1

#initialize our new image object
img = Image.new('RGB', (width, height))
pixel = img.load()

#populate the arrays
for x in range(width):
	for y in range(height):

		if randrange(2) == 0:
			soilGrid.append([])
			soilGridIndex += 1
			soilGrid[soilGridIndex].append(x)
			soilGrid[soilGridIndex].append(y)
			pixel[soilGrid[len(soilGrid) - 1][0], soilGrid[len(soilGrid) - 1][1]] = (153, 76, 0)

		else:
			treeGrid.append([])
			treeGridIndex += 1
			treeGrid[treeGridIndex].append(x)
			treeGrid[treeGridIndex].append(y)
			pixel[treeGrid[len(treeGrid) - 1][0], treeGrid[len(treeGrid) - 1][1]] = (0, 204, 0)

#timer for processing speed
startTime = time.time() 

#the main loop
for f in range(int(frames)):

	for i in range(len(treeGrid)):
		if (random() < 0.00000033) & (len(treeGrid) != 0):
			randNum = randrange(len(treeGrid))
			fireGrid.append(treeGrid[randNum])
			del treeGrid[randNum]
			pixel[fireGrid[len(fireGrid) - 1][0], fireGrid[len(fireGrid) - 1][1]] = (244, 66, 66) 

	for i in range(len(soilGrid)):
		if (random() < 0.002) & (len(soilGrid) != 0):
			randNum = randrange(len(soilGrid))
			treeGrid.append(soilGrid[randNum])
			del soilGrid[randNum]
			pixel[treeGrid[len(treeGrid) - 1][0], treeGrid[len(treeGrid) - 1][1]] = (0, 204, 0)

	for i in range(len(fireGrid)):
		if (random() < 0.1) & (len(fireGrid) != 0):
			randNum = randrange(len(fireGrid))
			soilGrid.append(fireGrid[randNum])
			del fireGrid[randNum]
			pixel[soilGrid[len(soilGrid) - 1][0], soilGrid[len(soilGrid) - 1][1]] = (153, 76, 0)
		elif (random() >= 0.1) & (len(fireGrid) != 0) & (len(treeGrid) != 0):
			try: # SORT THIS OUT, REMOVE TRY!
				for j in range(len(treeGrid)):
					for k in range(len(fireGrid)):
						if (fireGrid[k] in fireGrid) & (treeGrid[j] in treeGrid):

							absX = abs(treeGrid[j][0] - fireGrid[k][0])
							absY = abs(treeGrid[j][1] - fireGrid[k][1])

							if absX == 1 & absY == 1:
								fireGrid.append(treeGrid[k])
								del treeGrid[randNum]
								pixel[fireGrid[len(fireGrid) - 1][0], fireGrid[len(fireGrid) - 1][1]] = (244, 66, 66)
			except:
				pass 



	#save it
	img.save("img/"+str(f)+".png")
 
	percentageFrames = str(round((f+1)/frames * 100, 2))
	elapsedTime = time.time() - startTime
	fps = round((f+1)/elapsedTime, 2)
	eta = str(round((frames - (f + 1)) / fps, 2))
 
	print("{}/{}| {}% | FPS: {} | ETA: {}".format(f+ 1, frames, percentageFrames, fps, eta) , end='\r')

 
#make a video
videoSettings = "ffmpeg -r 30 -f image2 -s 1280x720 -i "
videoPath =  "img/%d.png"
videoCodex = " -vcodec libx264 -crf 25 -pix_fmt yuv420p "
videoOutput = "vid/out.mp4 -y -loglevel quiet"
subprocess.Popen(videoSettings+videoPath+videoCodex+videoOutput)
input()