from psychopy import visual,core,event,monitors
import numpy as np
import ColorTools as ct
import psychopy._shadersPyglet as shaders
import colorsys as cs

params = {}				
params['monitor_width'] = 48
params['monitor_viewdist'] = 60
params['monitor_pixelDims'] = (1280,1024)
params['screenSize'] = (1280,1024)		

mon = monitors.Monitor(name = 'dell', width = params['monitor_width'], distance = params['monitor_viewdist'])
mon.setSizePix(params['monitor_pixelDims'])

screen = visual.Window(params['screenSize'], units = 'deg', monitor = mon, color = (0, 0, 0), allowGUI = False)

colorToBlackFragmentShader = '''
   uniform sampler2D texture, mask;
   void main() {
	   vec4 textureFrag = texture2D(texture,gl_TexCoord[0].st);
	   vec4 maskFrag = texture2D(mask,gl_TexCoord[1].st);
	   gl_FragColor.a = gl_Color.a*maskFrag.a*textureFrag.a;
	   gl_FragColor.rgb = gl_Color.rgb * ((textureFrag.rgb +1.0)/2.0);
   }
   '''
if screen.winType=='pyglet' and screen._haveShaders:
   screen._progSignedTexMask = shaders.compileProgram(shaders.vertSimple,
colorToBlackFragmentShader)
#end 				

base_lum = 0.5
base_sat = 1.0

# orientations = np.linspace(90.0, 270.0, 9)
# orientations = orientations[0:7]
# colors = np.linspace(0.0, 1.0, 9)
# colors = colors[0:7]	 

# colors = ((75, -80, 0),
		  # (75, -50, 50),
		  # (75, 0, 80),
		  # (75, 50, 50),
		  # (75, 80, 0),
		  # (75, 50, -50),
		  # (75, 0, -80),
		  # (75, -50, -50))


# xpos = np.linspace(-16.0, 16.0, 8)
# ypos = np.linspace(-16.0, 16.0, 8)

o = 45.0
x = 0
y = 0

stim_array = []
c= (70,110,76.8)
stim_array.append(visual.GratingStim(screen, tex='sqr', mask='raisedCos', maskParams = {'fringeWidth': 0.6}, texRes = 1024, sf = 1.0, ori = o,  size = 5, pos = (x,y), colorSpace = 'rgb', color = ct.lab2psycho(c)))


# for o, y in zip(orientations, xpos):
	# for c, x in zip(colors, ypos):
		# #stim_array.append(visual.GratingStim(screen, tex = 'sin', mask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, texRes = 1024, sf = 1.0, ori = o,  size = 1.5, pos = (x,y), colorSpace = 'rgb255', color = [rgbc*255.0 for rgbc in cs.hls_to_rgb(c,base_lum,base_sat)]))
		# stim_array.append(visual.GratingStim(screen, tex = 'sin', mask = 'raisedCos', maskParams = {'fringeWidth': 0.6}, texRes = 1024, sf = 1.0, ori = o,  size = 1.5, pos = (x,y), colorSpace = 'rgb', color = ct.lab2psycho(c)))

for stim in stim_array:
	stim.draw()


screen.flip()

event.waitKeys()

screen.close()
# # HSL colorlist
# colorlist = ((1,-1,-1),
# 			 (1,1,-1),
# 			 (-1,1,-1),
# 			 (-1,1,1),
# 			 (-1,-1,1),
# 			 (1,-1,1)