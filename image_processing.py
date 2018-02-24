import numpy as np
from PIL import Image

def rotation90(img_file="static/img/temp_img.jpeg"):
    print("RUNNED!!!!")
    img = Image.open(img_file)
    img = img.convert("RGB")
    img_arr = np.asarray(img)

    rotated90 = np.zeros((img_arr.shape[1], img_arr.shape[0], img_arr.shape[2]))
    rotated90.setflags(write=1)

    for row in range(img_arr.shape[0]):
        for col in range(img_arr.shape[1]):
            rotated90[col, -1 * (row + 1), :] = img_arr[row,col,:]

    img_new = Image.fromarray(rotated90.astype('uint8'))
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_rotated.jpeg")
    print("SAVED!!!")

def rotation180():
    rotation90()
    rotation90("static/img/temp_img_rotated.jpeg")

def rotation270():
    rotation180()
    rotation90("static/img/temp_img_rotated.jpeg")