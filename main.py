import os, numpy
from PIL import Image

SKINS_FOLDER = "path/to/../minecraft/assets/skins"
AMOUNT = 1000
INITIAL_IMAGE = Image.new("RGBA", (64, 64))
SCALE = 1

def find_all_files(path, amount = 100000):
  result = []
  for root, dirs, files in os.walk(path):
  	for i, name in enumerate(files):
  		if i > amount:
  			break
  		elif not name.startswith( '.' ):
  			result.append(os.path.join(root, name))
  return result

image_paths = find_all_files(SKINS_FOLDER)

blendable_paths = []
for i, filename in enumerate(image_paths):
	try:
		temp_image = Image.open(filename)
		if (INITIAL_IMAGE.size == temp_image.size) and (INITIAL_IMAGE.mode == temp_image.mode):
			blendable_paths.append(filename)
		temp_image.close()
	except BaseException as err:
		print('Could not load', filename, 'because of', err)

INITIAL_WIDTH, INITIAL_HEIGHT = INITIAL_IMAGE.size

pixel_array = numpy.zeros((INITIAL_HEIGHT, INITIAL_WIDTH, 4), numpy.float)

try:
    AMOUNT
except NameError:
    AMOUNT_NEW = len(blendable_paths)
else:
    AMOUNT_NEW = AMOUNT

for i, path in enumerate(blendable_paths):
	print(i+1, path)
	im_array = numpy.array(Image.open(path), dtype=numpy.float)
	pixel_array = pixel_array + im_array / AMOUNT_NEW
	if (i >= AMOUNT_NEW - 1):
		break

pixel_array = numpy.array(numpy.round(pixel_array), dtype=numpy.uint8)

output = Image.fromarray(pixel_array, mode="RGBA")

print(output.format, output.size, output.mode)
output.resize((64 * SCALE, 64 * SCALE)).save("averaged.png")

# output.save("averaged.png")