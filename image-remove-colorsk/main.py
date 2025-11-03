from PIL import Image
import numpy as np

# img_file = '1.png'
img_file = '2.sub.png'
color = (255, 0, 255)


img = Image.open(img_file)
data = np.array(img)
converted = np.where(data == color[0], color[1], color[2])
img = Image.fromarray(converted.astype('uint8'))

img.save(img_file[:-4] + '-removed-color' + img_file[-4:])

