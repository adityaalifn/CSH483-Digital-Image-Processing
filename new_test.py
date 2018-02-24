import numpy as np
from PIL import Image

# # Flip
# img = Image.open("static/img/image_here.jpg")
# img = img.convert("RGB")
# img_arr = np.asarray(img)

# rotated90 = img_arr.copy()
# rotated90.setflags(write=1)

# for row in range(img_arr.shape[0]):
#     for col in range(img_arr.shape[1]):
#         rotated90[-1 * (row + 1), col, 0] = img_arr[row, col, 0]
#         rotated90[-1 * (row + 1), col, 1] = img_arr[row, col, 1]
#         rotated90[-1 * (row + 1), col, 2] = img_arr[row, col, 2]

# img_new = Image.fromarray(rotated90)
# img_new = img_new.convert("RGB")
# img_new.show()

# ROTASI
img = Image.open("static/img/image_here.jpg")
img = img.convert("RGB")
img_arr = np.asarray(img)

rotated90 = np.zeros((img_arr.shape[1], img_arr.shape[0], img_arr.shape[2]))
rotated90.setflags(write=1)

for row in range(img_arr.shape[0]):
    for col in range(img_arr.shape[1]):
        rotated90[col, -1 * (row + 1), :] = img_arr[row, col, :]

img_new = Image.fromarray(rotated90.astype('uint8'))
img_new = img_new.convert("RGB")
img_new.show()
