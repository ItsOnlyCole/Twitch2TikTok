from moviepy.editor import *
import sys
import cv2

clipFile = sys.argv[1]
clipName = clipFile[0:-4]

def blur(image):
    return cv2.GaussianBlur(image, (99,99), cv2.BORDER_DEFAULT)

#Creates a blank color clip that is used to set the resolution
def createResolutionClip():
    return ColorClip((1080,1920), (0,0,0), duration=1)

#Setup background clip
def createBackgroundClip(originalClip):
    clip = VideoFileClip(originalClip).fx(vfx.resize, width=3413)
    clip = clip.fl_image(blur)
    clip = clip.set_position('center')
    return clip
#Sets up focus clip
def createFocusClip(originalClip):
    clip = VideoFileClip(originalClip).fx(vfx.resize, width=1080)
    clip = clip.set_position('center')
    return clip


if __name__ == '__main__':
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
