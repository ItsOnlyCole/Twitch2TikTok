from moviepy.editor import *
import sys
import cv2

clipFile = sys.argv[1]
clipName = clipFile[0:-4]

def blur(image):
    return cv2.GaussianBlur(image, (99,99), cv2.BORDER_DEFAULT)


#Creates a blank color clip that's used to set the resolution
resolutionClip = ColorClip((1080,1920), (0,0,0), duration=1)
#Background clip is set to fill screen and blurred
backgroundClip = VideoFileClip(clipFile).fx( vfx.resize, width=3413)
backgroundClip = backgroundClip.fl_image(blur)
backgroundClip = backgroundClip.set_position('center')
#Center Focus clip
focusClip = VideoFileClip(clipFile).fx( vfx.resize, width=1080 )
focusClip = focusClip.set_position('center')


#Combines clips and renders
### Clips stack bottom to top
final_clip = CompositeVideoClip([resolutionClip, backgroundClip, focusClip])
final_clip.write_videofile(clipName+"TikTok.mp4")
