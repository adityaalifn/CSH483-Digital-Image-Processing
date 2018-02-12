import numpy as np
from PIL import Image

img = Image.open("static/img/temp_img.png")
img = img.convert("RGB")

img_arr = np.asarray(img)
r = img_arr[:,:,0]
g = img_arr[:,:,1]
b = img_arr[:,:,2]

sum_r = np.sum(r)
sum_g = np.sum(g)
sum_b = np.sum(b)
# print(r, r*0.5)

if sum_r > sum_g and sum_r > sum_b:
    arr_gray = (0.5 * r) + (0.25 * g) + (0.25 * b)
elif sum_g > sum_r and sum_g > sum_b:
    arr_gray = (0.25 * r) + (0.5 * g) + (0.25 * b)
else:
    arr_gray = (0.25 * r) + (0.25 * g) + (0.5 * b)

img_new = Image.fromarray(arr_gray)
img_new = img_new.convert("RGB")
img_new.save("Gray.jpeg")
img_new.show()