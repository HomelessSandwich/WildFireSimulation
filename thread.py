from PIL import Image, ImageDraw
from threading import Thread as worker
import random, time, subprocess, queue

def Update(newForestGrid, forestGrid, width, height, frames, q):

	#update grid
	for f in range(int(frames - 1)):
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
		q.put(forestGrid)
	print("Thread 1 done")

			 
def Draw(width, height, frames, startTime, q):
	for f in range(int(frames - 1)):
		for x in range(width):
			for y in range(height):
				
					#initialize our new image object
				img = Image.new('RGB', (width, height))
				pixel = img.load()

				forestGrid = q.get()

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
				eta = str(round((frames - (f + 1)) / fps, 4))
			 
				print("{}/{}| {}% | FPS: {} | ETA: {}".format(f+ 1, frames, percentageFrames, fps, eta) , end='\r')
				#delete objects
				del img
		print("Thread 2 done")
		print()

def Populate(frames, width, height):
	#initialize arrays
	forestGrid = []
	newForestGrid = []

	#populate the arrays
	for x in range(width):
		forestGrid.append([])
		for y in range(height):
			if random.randrange(2) == 0:
				forestGrid[x].append(1)
			else:
				forestGrid[x].append(0)
	return forestGrid
	
		 
#metadata for the images
width = 100
height = 100

frames = int(input("How many frames would you like the video to be: "))

forestGrid = Populate(frames, width, height)
newForestGrid = forestGrid

#timer for processing speed
startTime = time.time() 

q = queue.Queue()

#starting workers
t1 = worker(target = Update, args = (newForestGrid, forestGrid, width, height, frames, q))
t2 = worker(target = Draw, args = (width, height, frames, startTime, q))

#t1.daemon = True
#t2.daemon = True

t1.start()
t2.start()
t1.join()
t2.join()

#make a video
videoSettings = "ffmpeg -r 30 -f image2 -s 1280x720 -i "
videoPath =  "img/%d.png"
videoCodex = " -vcodec libx264 -crf 25 -pix_fmt yuv420p "
videoOutput = "vid/out.mp4 -y -loglevel quiet"
subprocess.Popen(videoSettings+videoPath+videoCodex+videoOutput)