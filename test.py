# import numpy as np
# from PIL import Image

# img = Image.open("static/img/temp_img.jpeg")
# img = img.convert("RGB")

# img_arr = np.asarray(img)
# #img_arr.setflags(write=1)
# new_size = ((img_arr.shape[0]//2), (img_arr.shape[1]//2), img_arr.shape[2])
# new_arr = np.full(new_size, 255)
# print(img_arr.shape, new_size)
# new_arr.setflags(write=1)

# img_arr_shape = img_arr.shape

# for row in range(img_arr_shape[0]):
#     for col in range(img_arr_shape[1]):
#         try:
#             new_arr[row,col,0] = (int(img_arr[row,col,0]) + int(img_arr[row+1,col,0]) + int(img_arr[row,col+1,0]) + int(img_arr[row+1,col+1,0])) // 4
#             new_arr[row,col,1] = (int(img_arr[row,col,1]) + int(img_arr[row+1,col,1]) + int(img_arr[row,col+1,1]) + int(img_arr[row+1,col+1,1])) // 4
#             new_arr[row,col,2] = (int(img_arr[row,col,2]) + int(img_arr[row+1,col,2]) + int(img_arr[row,col+1,2]) + int(img_arr[row+1,col+1,2])) // 4
#         except:
#             break
#         col += 1
#     row += 1

# new_arr = np.uint8(new_arr)
# img_new = Image.fromarray(new_arr)
# #img_new = img_new.convert("RGB")
# img_new.show()


# Zoom Out
# import numpy as np
# from PIL import Image

# img = Image.open("static/img/temp_img.jpeg")
# img = img.convert("RGB")

# img_arr = np.asarray(img)

# img_arr_shape = img_arr.shape
# arr_x_size = img_arr.shape[0] * 4
# arr_y_size = img_arr.shape[1] * 4

# new_arr = np.full((arr_x_size, arr_y_size, 3), 255)
# new_arr.setflags(write=1)


# for row in range(img_arr_shape[0]):
#     for col in range(img_arr_shape[1]):
#         pix_1, pix_2, pix_3 = img_arr[row,col,0],img_arr[row,col,0],img_arr[row,col,0]
#         new_arr[row, col, 0], new_arr[row+1, col, 0], new_arr[row, col+1, 0], new_arr[row+1, col+1, 0] = pix_1, pix_1,pix_1,pix_1
#         new_arr[row, col, 1], new_arr[row+1, col, 1], new_arr[row, col+1, 1], new_arr[row+1, col+1, 1] = pix_2, pix_2,pix_2,pix_2
#         new_arr[row, col, 2], new_arr[row+1, col, 2], new_arr[row, col+1, 2], new_arr[row+1, col+1, 2] = pix_3, pix_3,pix_3,pix_3
#         col += 1
#     row += 1

# print(new_arr)
# new_arr = np.uint8(new_arr)
# img_new = Image.fromarray(new_arr)
# img_new = img_new.convert("RGB")
# img_new.show()


# Flip Horizontal
# import numpy as np
# from PIL import Image

# img = Image.open("static/img/temp_img.jpeg")
# img = img.convert("RGB")

# img_arr = np.asarray(img)

# flipped_arr = np.fliplr(img_arr)

# img_new = Image.fromarray(flipped_arr)
# img_new = img_new.convert("RGB")
# img_new.show()


# Brightness by add 100
# import numpy as np
# from PIL import Image

# img = Image.open("static/img/temp_img.jpeg")
# img = img.convert("RGB")

# img_arr = np.asarray(img)
# new_arr = img_arr * 2

# new_new_arr = np.where(((img_arr*2)-new_arr) > 255,255,None)

# img_new = Image.fromarray(new_arr)
# img_new = img_new.convert("RGB")
# img_new.show()

# Penggelapan
# import numpy as np
# from PIL import Image

# img = Image.open("static/img/temp_img.jpeg")
# img = img.convert("RGB")
# img_arr = np.asfarray(img)

# new_arr = img_arr - 100
# new_arr = np.clip(new_arr, 0, 255)

# img_new = Image.fromarray(new_arr.astype('uint8'))
# img_new = img_new.convert("RGB")
# img_new.show()

# Histrogram
# import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt

# img = Image.open("static/img/temp_img.jpeg")
# img = img.convert("RGB")
# img_arr = np.asarray(img)

# temp_r = np.zeros(256)
# temp_g = np.zeros(256)
# temp_b = np.zeros(256)

# for row in img_arr:
#     for col in row:
#         temp_r[col[0]] = temp_r[col[0]] + 1
#         temp_g[col[1]] = temp_g[col[1]] + 1
#         temp_b[col[2]] = temp_b[col[2]] + 1

# x = [i for i in range(256)]
# width = 1/1.5
# plt.bar(x,temp_r,width, color="r")
# plt.title("Red Histogram")
# plt.savefig("static/img/temp_red_hist.jpeg")
# plt.clf()

# plt.bar(x,temp_g,width, color="g")
# plt.title("Green Histogram")
# plt.savefig("static/img/temp_green_hist.jpeg")
# plt.clf()

# plt.bar(x,temp_b,width, color="b")
# plt.title("Blue Histogram")
# plt.savefig("static/img/temp_blue_hist.jpeg")
# plt.clf()

# import cv2
# import numpy as np


# def get8n(x, y, shape):
#     out = []
#     maxx = shape[1]-1
#     maxy = shape[0]-1

#     # top left
#     outx = min(max(x-1, 0), maxx)
#     outy = min(max(y-1, 0), maxy)
#     out.append((outx, outy))

#     # top center
#     outx = x
#     outy = min(max(y-1, 0), maxy)
#     out.append((outx, outy))

#     # top right
#     outx = min(max(x+1, 0), maxx)
#     outy = min(max(y-1, 0), maxy)
#     out.append((outx, outy))

#     # left
#     outx = min(max(x-1, 0), maxx)
#     outy = y
#     out.append((outx, outy))

#     # right
#     outx = min(max(x+1, 0), maxx)
#     outy = y
#     out.append((outx, outy))

#     # bottom left
#     outx = min(max(x-1, 0), maxx)
#     outy = min(max(y+1, 0), maxy)
#     out.append((outx, outy))

#     # bottom center
#     outx = x
#     outy = min(max(y+1, 0), maxy)
#     out.append((outx, outy))

#     # bottom right
#     outx = min(max(x+1, 0), maxx)
#     outy = min(max(y+1, 0), maxy)
#     out.append((outx, outy))

#     return out


# def region_growing(img, seed):
#     list = []
#     outimg = np.zeros_like(img)
#     list.append((seed[0], seed[1]))
#     processed = []
#     while(len(list) > 0):
#         pix = list[0]
#         outimg[pix[0], pix[1]] = 255
#         for coord in get8n(pix[0], pix[1], img.shape):
#             if img[coord[0], coord[1]] != 0:
#                 outimg[coord[0], coord[1]] = 255
#                 if not coord in processed:
#                     list.append(coord)
#                 processed.append(coord)
#         list.pop(0)
#         # cv2.imshow("progress",outimg)
#         # cv2.waitKey(1)
#     return outimg


# def on_mouse(event, x, y, flags, params):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print('Seed: ' + str(x) + ', ' + str(y), img[y, x])
#         clicks.append((y, x))


# clicks = []
# image = cv2.imread('/media/tabul/DATA/!Telkom University/CSH483-Digital-Image-Processing/static/img/temp_img.jpeg', 0)
# ret, img = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
# cv2.namedWindow('Input')
# cv2.setMouseCallback('Input', on_mouse, 0, )
# cv2.imshow('Input', img)
# cv2.waitKey()
# seed = clicks[-1]
# out = region_growing(img, seed)
# cv2.imshow('Region Growing', out)
# cv2.waitKey()
# cv2.destroyAllWindows()

import numpy as np
from PIL import Image

ptsX, ptsY = 20, 20
img = Image.open("static/img/temp_img.jpeg")
img = img.convert("RGB")

img_arr = np.asarray(img)
h, w, _ = img_arr.shape
