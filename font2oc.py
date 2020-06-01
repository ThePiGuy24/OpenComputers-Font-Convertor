import pygame, sys, os, requests

referencefontpath = "https://raw.githubusercontent.com/MightyPirates/OpenComputers/master-MC1.7.10/src/main/resources/assets/opencomputers/font.hex" # original font.hex, to know which characters to render

if len(sys.argv) < 1:
	print("Usage: font2oc <fontname> [font size] [x offset] [y offset]\n    font will be outputted in cwd as font.hex")
	sys.exit()

if len(sys.argv) > 2:
	fontsize = int(sys.argv[2])
else:
	fontsize = 16

if len(sys.argv) > 3:
	xoffset = int(sys.argv[3])
else:
	xoffset = 0

if len(sys.argv) > 4:
        yoffset = int(sys.argv[4])
else:
        yoffset = 0


pygame.init()

if os.path.exists(sys.argv[1]):
        fontpath = sys.argv[1]
else:
        fontpath = pygame.font.match_font(sys.argv[1])

print("Fetching Reference font.hex...")
r = requests.get(referencefontpath)
print("Decoding font.hex...")
fontlines = r.text.split("\n")
fontdict = {}
for line in fontlines:
	#print(line)
	try:
		key, data = line.split(":",1)
		fontdict[int(key,16)] = len(data)//4 # get character width
	except:
		continue
print("Loaded {0} Characters.".format(len(fontdict)))

font = pygame.font.Font(fontpath, fontsize)

def padhex(num, length):
	text = hex(num)[2:]
	return "0"*(length-len(text))+text.upper()

print("Rendering Font...")
with open("font.hex", "w") as fontfile:
	for char in fontdict:
		try:
			pixels = pygame.PixelArray(font.render(chr(char),False,(255,255,255),(0,0,0)))
		except (TypeError, UnicodeError, ValueError, pygame.error):
			pixels = pygame.PixelArray(font.render("?",False,(255,255,255),(0,0,0)))
		fontfile.write(padhex(char,4)+":")
		for y in range(16):
			line = 0
			for x in range(8):
				try:
					line = line * 2 + int(pixels[x+xoffset,y+yoffset] > 0)
				except IndexError:
					line = line * 2
			fontfile.write(padhex(line,2))
		if fontdict[char] > 8:
			for y in range(16):
				line = 0
				for x in range(8,16):
                                	try:
                                        	line = line * 2 + int(pixels[x+xoffset,y+yoffset] > 0)
                                	except IndexError:
                                        	line = line * 2
				fontfile.write(padhex(line,2))
		fontfile.write("\n")
print("Done!")
