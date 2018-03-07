import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def grayscale():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")

    img_arr = np.asarray(img)
    r = img_arr[:, :, 0]
    g = img_arr[:, :, 1]
    b = img_arr[:, :, 2]

    sum_r = np.sum(r)
    sum_g = np.sum(g)
    sum_b = np.sum(b)
    sum_all = sum_r + sum_g + sum_b
    # print(r, r*0.5)

    arr_gray = (sum_r / sum_all * r) + \
        (sum_g / sum_all * g) + (sum_b / sum_all * b)

    # if sum_r > sum_g and sum_r > sum_b:
    #     arr_gray = (0.5 * r) + (0.25 * g) + (0.25 * b)
    # elif sum_g > sum_r and sum_g > sum_b:
    #     arr_gray = (0.25 * r) + (0.5 * g) + (0.25 * b)
    # else:
    #     arr_gray = (0.25 * r) + (0.25 * g) + (0.5 * b)

    img_new = Image.fromarray(arr_gray)
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_grayscale.jpeg")


def invers():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")

    img_arr = np.asarray(img)
    img_arr.setflags(write=1)
    img_arr[:, :, 0] = 255 - img_arr[:, :, 0]
    img_arr[:, :, 1] = 255 - img_arr[:, :, 1]
    img_arr[:, :, 2] = 255 - img_arr[:, :, 2]

    img_new = Image.fromarray(img_arr)
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_inverse.jpeg")


def zoomin():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")

    img_arr = np.asarray(img)
    # img_arr.setflags(write=1)
    new_size = ((img_arr.shape[0] // 2),
                (img_arr.shape[1] // 2), img_arr.shape[2])
    new_arr = np.full(new_size, 255)
    print(img_arr.shape, new_size)
    new_arr.setflags(write=1)

    img_arr_shape = img_arr.shape

    for row in range(img_arr_shape[0]):
        for col in range(img_arr_shape[1]):
            try:
                new_arr[row, col, 0] = (int(img_arr[row, col, 0]) + int(img_arr[row + 1, col, 0]) + int(
                    img_arr[row, col + 1, 0]) + int(img_arr[row + 1, col + 1, 0])) // 4
                new_arr[row, col, 1] = (int(img_arr[row, col, 1]) + int(img_arr[row + 1, col, 1]) + int(
                    img_arr[row, col + 1, 1]) + int(img_arr[row + 1, col + 1, 1])) // 4
                new_arr[row, col, 2] = (int(img_arr[row, col, 2]) + int(img_arr[row + 1, col, 2]) + int(
                    img_arr[row, col + 1, 2]) + int(img_arr[row + 1, col + 1, 2])) // 4
            except:
                break
            col += 1
        row += 1

    new_arr = np.uint8(new_arr)
    img_new = Image.fromarray(new_arr)
    img_new.save("static/img/temp_img_zoomin.jpeg")


def zoomout():
    zoomin()
    img = Image.open("static/img/temp_img_zoomin.jpeg")
    img = img.convert("RGB")

    img_arr = np.asarray(img)

    img_arr_shape = img_arr.shape
    arr_x_size = img_arr.shape[0] * 2
    arr_y_size = img_arr.shape[1] * 2

    new_arr = np.full((arr_x_size, arr_y_size, 3), 255)
    new_arr.setflags(write=1)

    for row in range(img_arr_shape[0]):
        for col in range(img_arr_shape[1]):
            pix_1, pix_2, pix_3 = img_arr[row, col,
                                          0], img_arr[row, col, 1], img_arr[row, col, 2]
            new_arr[row, col, 0], new_arr[row + 1, col, 0], new_arr[row, col +
                                                                    1, 0], new_arr[row + 1, col + 1, 0] = pix_1, pix_1, pix_1, pix_1
            new_arr[row, col, 1], new_arr[row + 1, col, 1], new_arr[row, col +
                                                                    1, 1], new_arr[row + 1, col + 1, 1] = pix_2, pix_2, pix_2, pix_2
            new_arr[row, col, 2], new_arr[row + 1, col, 2], new_arr[row, col +
                                                                    1, 2], new_arr[row + 1, col + 1, 2] = pix_3, pix_3, pix_3, pix_3
            col += 1
        row += 1

    # print(new_arr)
    new_arr = np.uint8(new_arr)
    img_new = Image.fromarray(new_arr)
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_zoomout.jpeg")


def crop():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")

    img_arr = np.asarray(img)
    img_arr.setflags(write=1)

    middle_x = img_arr.shape[0]
    middle_y = img_arr.shape[1]

    middle_x_start = middle_x * 1 // 4
    middle_x_end = middle_x * 3 // 4

    middle_y_start = middle_y * 1 // 4
    middle_y_end = middle_y * 3 // 4

    img_arr = img_arr[middle_x_start:middle_x_end,
                      middle_y_start:middle_y_end, :]
    img_new = Image.fromarray(img_arr)
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_crop.jpeg")


def flipvertical():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)

    flipped_arr = img_arr.copy()
    flipped_arr.setflags(write=1)

    for row in range(img_arr.shape[0]):
        for col in range(img_arr.shape[1]):
            flipped_arr[-1 * (row + 1), col, 0] = img_arr[row, col, 0]
            flipped_arr[-1 * (row + 1), col, 1] = img_arr[row, col, 1]
            flipped_arr[-1 * (row + 1), col, 2] = img_arr[row, col, 2]

    img_new = Image.fromarray(flipped_arr)
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_flipvertical.jpeg")


def fliphorizontal():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)

    flipped_arr = img_arr.copy()
    flipped_arr.setflags(write=1)

    for row in range(img_arr.shape[0]):
        for col in range(img_arr.shape[1]):
            flipped_arr[row, -1 * (col + 1), 0] = img_arr[row, col, 0]
            flipped_arr[row, -1 * (col + 1), 1] = img_arr[row, col, 1]
            flipped_arr[row, -1 * (col + 1), 2] = img_arr[row, col, 2]

    img_new = Image.fromarray(flipped_arr)
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_fliphorizontal.jpeg")


def brightnesswithincrease(val=0):
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")
    img_arr = np.asfarray(img)

    new_arr = img_arr + int(val)
    new_arr = np.clip(new_arr, 0, 255)

    img_new = Image.fromarray(new_arr.astype('uint8'))
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_brightnesswithincrease.jpeg")


def brightnesswithmultiply(val=0):
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")
    img_arr = np.asfarray(img)

    new_arr = img_arr * int(val)
    new_arr = np.clip(new_arr, 0, 255)

    img_new = Image.fromarray(new_arr.astype('uint8'))
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_brightnesswithmultiply.jpeg")


def darkeningwithdecrease(val=0):
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")
    img_arr = np.asfarray(img)

    new_arr = img_arr - int(val)
    new_arr = np.clip(new_arr, 0, 255)

    img_new = Image.fromarray(new_arr.astype('uint8'))
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_darkeningwithdecrease.jpeg")


def darkeningwithdivide(val=0):
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")
    img_arr = np.asfarray(img)

    new_arr = img_arr // int(val)
    new_arr = np.clip(new_arr, 0, 255)

    img_new = Image.fromarray(new_arr.astype('uint8'))
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_darkeningwithdivide.jpeg")


def rotation90(img_file="static/img/temp_img.jpeg"):
    # print("RUNNED!!!!")
    img = Image.open(img_file)
    img = img.convert("RGB")
    img_arr = np.asarray(img)

    rotated90 = np.zeros(
        (img_arr.shape[1], img_arr.shape[0], img_arr.shape[2]))
    rotated90.setflags(write=1)

    for row in range(img_arr.shape[0]):
        for col in range(img_arr.shape[1]):
            rotated90[col, -1 * (row + 1), :] = img_arr[row, col, :]

    img_new = Image.fromarray(rotated90.astype('uint8'))
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_rotated.jpeg")
    # print("SAVED!!!")


def rotation180():
    rotation90()
    rotation90("static/img/temp_img_rotated.jpeg")


def rotation270():
    rotation180()
    rotation90("static/img/temp_img_rotated.jpeg")


def histogram():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)

    temp_r = np.zeros(256)
    temp_g = np.zeros(256)
    temp_b = np.zeros(256)

    for row in img_arr:
        for col in row:
            temp_r[col[0]] += 1
            temp_g[col[1]] += 1
            temp_b[col[2]] += 1

    x = [i for i in range(256)]
    width = 1 / 1.5
    # plt.plot(x, temp_r)
    plt.bar(x, temp_r, width, color="r")
    plt.title("Red Histogram")
    plt.savefig("static/img/temp_red_hist.jpeg")
    plt.clf()

    # plt.plot(x, temp_g)
    plt.bar(x, temp_g, width, color="g")
    plt.title("Green Histogram")
    plt.savefig("static/img/temp_green_hist.jpeg")
    plt.clf()

    # plt.plot(x, temp_b)
    plt.bar(x, temp_b, width, color="b")
    plt.title("Blue Histogram")
    plt.savefig("static/img/temp_blue_hist.jpeg")
    plt.clf()


def convolute():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)

    h, w, c = img_arr.shape

    temp = np.zeros_like(img_arr)
    ker = np.array(([-1, -1, -1],
                    [-1, 8, -1],
                    [-1, -1, -1]), dtype="int")

    for i in range(1, h - 1):
        for j in range(1, w - 1):
            for k in range(c):
                temp[i, j, k] = img_arr[i - 1, j - 1, k] * ker[0, 0] + img_arr[i - 1, j, k] * ker[0, 1] + img_arr[i - 1, j + 1, k] * ker[0, 2] + img_arr[i, j - 1, k] * ker[1, 0] + \
                    img_arr[i, j, k] * ker[1, 1] + img_arr[i, j + 1, k] * ker[1, 2] + img_arr[i + 1, j - 1,
                                                                                              k] * ker[2, 0] + img_arr[i + 1, j, k] * ker[2, 1] + img_arr[i + 1, j + 1, k] * ker[2, 2]
    img_new = Image.fromarray(temp.astype('uint8'))
    img_new = img_new.convert("RGB")
    img_new.show()
    # img_arr_shape = img_arr.shape
    # x_zeros = np.zeros[img_arr_shape[1]]
    # y_zeros = np.zeros(img_arr_shape[0])

    # img_arr.setflags(write=1)
    # laplacian = np.array((
    # [0, 1, 0],
    # [1, -4, 1],
    # [0, 1, 0]), dtype="int")

convolute()