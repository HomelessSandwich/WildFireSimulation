from PIL import Image, ImageDraw
import yaml, random, time, subprocess, os, datetime

#open our configuration file
with open('config.yaml', 'r') as f:
    config = yaml.load(f)
print(config)

#load the size from the config
size = (config['img']['width'], config['img']['height'])

#get the path
path = os.path.dirname(os.path.realpath(__file__))

#initialize our arrays
old = []
new = []

#populate the arrays
for x in range(0, config['img']['width']):
    old.append([])
    for y in range(0, config['img']['height']):
        if random.randint(0,2) == 0:
            old[x].append("green")
        else:
            old[x].append("empty")
new = old

#the main loop
for f in range(0, config['sim']['frames']):

    #initialize our new image object
    im = Image.new('RGBA', size)
    draw = ImageDraw.Draw(im)

    #update the old list
    old = new

    #update everything
    for x in range(0, config['img']['width']):
        for y in range(0, config['img']['height']):
            if old[x][y] == 'green':
                #set on fire
                if random.randint(0,3000000) == 12:
                    new[x][y] = 'red'

            elif old[x][y] == 'empty':
                #grow a tree
                if random.randint(0,500) == 1:
                    new[x][y] = 'green'

            elif old[x][y] == 'red':
                #tree burns away
                if random.randint(0,10) == 1:
                    new[x][y] = 'empty'
                #the fire spreads out
                else:
                    for dx in range(-1,2):
                        for dy in range(-1,2):
                            #print(dx,dy)
                            #time.sleep(1)
                            if (dx != 0) & (dy != 0):
                                #print('set on fire')
                                try:
                                    if (old[x + dx][y + dy] == 'green'):
                                        new[x + dx][y + dy] = 'red'
                                except:
                                    pass




    #draw everything
    for x in range(0, config['img']['width']):
        for y in range(0, config['img']['height']):
            if new[x][y] == "green":
                draw.point([(x,y)],(134, 244, 66))
            elif new[x][y] == "empty":
                draw.point([(x,y)],(0,0,0))
            elif new[x][y] == "red":
                draw.point([(x,y)],(244, 66, 66))
        #print(str(round(x / int(config['img']['width']) * 100,2)) + " % completed" )

    draw.text((10,10), str(f), fill=(244, 66, 212))

    #delete the drawer
    del draw

    #save it
    im.save("img/"+str(f)+".png")
    print(str(f)+"|"+str(config['sim']['frames']))

#make a video
videoCommand = "ffmpeg -r 30 -f image2 -s 640x480 -i %d.png -vcodec libx264 -crf 15 "
videoOutput = "../video/out.mp4 -y"
subprocess.Popen(["cd img; "+videoCommand+videoOutput+"; cd ..; rm img/*; cd video; mv out.mp4 "+str(time.time())+".mp4"], shell=True).wait()
