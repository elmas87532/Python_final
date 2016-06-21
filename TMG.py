# -*- coding: utf-8 -*-
from moviepy.editor import *
import sys
from PIL import Image, ImageSequence
import ImageDraw
from images2gif import writeGif
import os

clip1 = (VideoFileClip("D:\\tmpdisk\\rs.mp4")
        .subclip((1,39.00),(1,40.00))
        .resize(0.3))
clip1.write_gif("r1.gif")
clip2 = (VideoFileClip("D:\\tmpdisk\\rs.mp4")
        .subclip((3,20.00),(3,21.00))
        .resize(0.3))
clip2.write_gif("r2.gif")
clip3 = (VideoFileClip("D:\\tmpdisk\\rs.mp4")
        .subclip((7,9.00),(7,10.00))
        .resize(0.3))
clip3.write_gif("r3.gif")
clip4 = (VideoFileClip("D:\\tmpdisk\\rs.mp4")
        .subclip((7,30.00),(7,31.00))
        .resize(0.3))
clip4.write_gif("r4.gif")

print "VIDEO->GIF DONE"

rs = Image.open( "r1.gif" )
rsSize = rs.size
weight = rsSize[0]*2
height = rsSize[1]*2

im = Image.new( "RGB", (weight,height) )
draw = ImageDraw.Draw( im )
im.save("bg.png")

i=0

for n in range(1,5):
    fname="r%d.gif"%n
    pfname="r%d"%n
    img = Image.open(fname)
    pal = img.getpalette()
    prev = img.convert('RGBA')
    prev_dispose = True
    for i, frame in enumerate(ImageSequence.Iterator(img)):
        dispose = frame.dispose

        if frame.tile:
            x0, y0, x1, y1 = frame.tile[0][1]
            if not frame.palette.dirty:
                frame.putpalette(pal)
            frame = frame.crop((x0, y0, x1, y1))
            bbox = (x0, y0, x1, y1)
        else:
            bbox = None

        if dispose is None:
            prev.paste(frame, bbox, frame.convert('RGBA'))
            prev.save(pfname+'%02d.png' % i)
            prev_dispose = False
        else:
            if prev_dispose:
                prev = Image.new('RGBA', img.size, (0, 0, 0, 0))
            out = prev.copy()
            out.paste(frame, bbox, frame.convert('RGBA'))
            out.save(+pfname+'%02d.png' % i)

print "GIF->PNG DONE"
i = i+1
w = weight/2
h = height/2

baseim = Image.open( "bg.png" )

count=0

for n in range(1,i):
    #print n

    floatim1 = Image.open( "r1%02d.png" % n )
    baseim.paste( floatim1, (0, 0) )
    floatim2 = Image.open( "r2%02d.png" % n )
    baseim.paste( floatim2, (w, 0) )
    floatim3 = Image.open( "r3%02d.png" % n )
    baseim.paste( floatim3, (0, h) )
    floatim4 = Image.open( "r4%02d.png" % n )
    baseim.paste( floatim4, (w, h) )
    baseim.save( "pasted%2d.png" % n  )
    count=count+1

for n in range(0,count+1):
    os.remove("r1%02d.png" %n)
    os.remove("r2%02d.png" %n)
    os.remove("r3%02d.png" %n)
    os.remove("r4%02d.png" %n)
os.remove("bg.png")

print "PUZZLING PNG DONE"

####images--->gif####
file_names = sorted((fn for fn in os.listdir('.') if fn.endswith('.png')))
images = [Image.open(fn) for fn in file_names]


filename = "your.GIF"
writeGif(filename, images, duration=0)

print "FINAL GIF DONE"

for n in range(1,count+1):
    os.remove("pasted%2d.png" %n)

print "!!!WELL DONE!!!"


