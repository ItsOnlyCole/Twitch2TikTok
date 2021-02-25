from moviepy.editor import *
import sys
import cv2
import argparse

parser = argparse.ArgumentParser(description="Automate editing gameplay clips for Tik Tok")
parser.add_argument('-f', '--file', metavar='', required=True, help="file to edit and render")
parser.add_argument('-sc', '--start', metavar='', type=int, help="custom start time of clip in seconds")
parser.add_argument('-ec', '--end', metavar='', type=int, help="custom end time of clip in seconds")
parser.add_argument('-a', '--automate', action='store_true', help="automate script by having having file NAME_StartTime_EndTime.mp4")
args = parser.parse_args()


def blur(image):
    return cv2.GaussianBlur(image, (99,99), cv2.BORDER_DEFAULT)

#Creates a blank color clip that is used to set the resolution
def createResolutionClip():
    return ColorClip((1080,1920), (0,0,0), duration=1)

#Setup background clip
def createBackgroundClip(originalClip):
    clip = originalClip.fx(vfx.resize, width=3413)
    clip = clip.fl_image(blur)
    clip = clip.set_position("center")
    return clip
#Sets up focus clip
def createFocusClip(originalClip):
    clip = originalClip.fx(vfx.resize, width=1080)
    clip = clip.set_position("center")
    return clip
#Cuts the clip
def cutClip(originalClip, startTime, endTime):
     return originalClip.subclip(startTime, endTime)


if __name__ == '__main__':
    if(args.automate == True):
        stringParse = args.file.split("_")
        clipName = stringParse[0]
        try:
            args.start = stringParse[1]
        except IndexError:
            args.start = None
        try:
            endTimeParse = stringParse[2].split(".")
            args.end = endTimeParse[0]
        except IndexError:
            args.end = None
            startTimeParse = stringParse[1].split(".")
            args.start = startTimeParse[0]
    else:
        clipName = args.file[0:-4]

    originalClip = VideoFileClip(args.file)

    if((args.start != None) and (args.end != None)):
        originalClip = cutClip(originalClip, args.start, args.end)
    elif((args.start != None) and (args.end == None)):
        originalClip = cutClip(originalClip, args.start, originalClip.duration)
    elif((args.start == None) and (args.end != None)):
        originalClip = cutClip(originalClip, 0, args.end)

    resolutionClip = createResolutionClip()
    backgroundClip = createBackgroundClip(originalClip)
    focusClip = createFocusClip(originalClip)

    #Combines clips and renders
    ### Clips stack back to front
    final_clip = CompositeVideoClip([resolutionClip, backgroundClip, focusClip])
    final_clip.write_videofile(clipName+"TikTok.mp4")

    #Closing clips for cleanup
    resolutionClip.close()
    backgroundClip.close()
    focusClip.close()
