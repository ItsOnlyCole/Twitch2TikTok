from moviepy.editor import *
import sys
import cv2
import argparse

parser = argparse.ArgumentParser(description="Automate editing gameplay clips for Tik Tok")
parser.add_argument('-f', '--file', metavar='', required=True, help="file to edit and render")
parser.add_argument('-Sc', '--Start', metavar='', require=False, help="custom start time of clip")
parser.add_argument('-Ec', '--End', metavar='', require=False, help="custom end time of clip")
parser.add_argument('-a', '--automate', metavar='', required=False, action='store_true', help="automate script by having having file NAME_StartTime_EndTime.mp4")
args = parser.parse_args()


def blur(image):
    return cv2.GaussianBlur(image, (99,99), cv2.BORDER_DEFAULT)

#Creates a blank color clip that is used to set the resolution
def createResolutionClip():
    return ColorClip((1080,1920), (0,0,0), duration=1)

#Setup background clip
def createBackgroundClip(originalClip):
    clip = VideoFileClip(originalClip).fx(vfx.resize, width=3413)
    clip = clip.fl_image(blur)
    clip = clip.set_position("center")
    return clip
#Sets up focus clip
def createFocusClip(originalClip):
    clip = VideoFileClip(originalClip).fx(vfx.resize, width=1080)
    clip = clip.set_position("center")
    return clip


if __name__ == '__main__':
    clipFile = args.file
    clipName = clipFile[0:-4]

    resolutionClip = createResolutionClip()
    backgroundClip = createBackgroundClip(clipFile)
    focusClip = createFocusClip(clipFile)

    #Combines clips and renders
    ### Clips stack back to front
    final_clip = CompositeVideoClip([resolutionClip, backgroundClip, focusClip])
    final_clip.write_videofile(clipName+"TikTok.mp4")

    #Closing clips for cleanup
    resolutionClip.close()
    backgroundClip.close()
    focusClip.close()
