import numpy as np
from PIL import Image

img = Image.open("static/img/image_here.jpg")
img = img.convert("RGB")
img_arr = np.asarray(img)

flipped_arr = img_arr.copy()
flipped_arr.setflags(write=1)

for row in range(img_arr.shape[0]):
    for col in range(img_arr.shape[1]):
        flipped_arr[-1*(row+1), col, 0] = img_arr[row,col,0]
        flipped_arr[-1*(row+1), col, 1] = img_arr[row,col,1]
        flipped_arr[-1*(row+1), col, 2] = img_arr[row,col,2]
        
img_new = Image.fromarray(flipped_arr)
img_new = img_new.convert("RGB")
img_new.show()