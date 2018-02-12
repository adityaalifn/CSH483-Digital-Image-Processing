import numpy as np
from PIL import Image

img = Image.open("static/img/temp_img.jpeg")
img = img.convert("RGB")

img_arr = np.asarray(img)
img_arr.setflags(write=1)
img_arr[:, :, 0] = 255 - img_arr[:, :, 0]
img_arr[:, :, 1] = 255 - img_arr[:, :, 1]
img_arr[:, :, 2] = 255 - img_arr[:, :, 2]

img_new = Image.fromarray(img_arr)
# img_new = img_new.convert("RGB")
img_new.show()