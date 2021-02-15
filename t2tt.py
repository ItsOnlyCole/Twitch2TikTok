from moviepy.editor import *
import sys

clipFile = sys.argv[1]
clipName = clipFile[0:-4]


#Creates a blank color clip that's used to set the resolution
resolutionClip = ColorClip((1080,1920), (0,0,0), duration=1)
#Center Focus clip
focusClip = VideoFileClip(clipFile).fx( vfx.resize, width=1080 )
focusClip = focusClip.set_position('center')


#Combines clips and renders
### Clips stack bottom to top
final_clip = CompositeVideoClip([resolutionClip, focusClip])
final_clip.write_videofile(clipName+"TikTok.mp4")
