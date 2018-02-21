import numpy as np
from PIL import Image
import os
from flask import Flask, render_template, request, make_response
from datetime import datetime
from functools import wraps, update_wrapper

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@app.route("/index")
@app.route("/")
@nocache
def index():
    return render_template("home.html", file_path="img/image_here.jpg")


@app.route("/brightness")
@nocache
def brightness():
    return render_template("brightness.html", file_path="img/temp_img.jpeg")


@app.route("/darkening")
@nocache
def darkening():
    return render_template("darkening.html", file_path="img/temp_img.jpeg")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/about")
@nocache
def about():
    return render_template("about.html")


@app.route("/upload", methods=["POST"])
@nocache
def upload():
    target = os.path.join(APP_ROOT, "static/img")
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        if file.filename == "":
            return render_template("no_img.html", file_path="img/no_image_selected.gif")

        # filename = "temp_img." + file.filename.split(".")[-1]
        filename = "temp_img.jpeg"
        destination = "/".join([target, filename])
        print(destination)
        file.save("static/img/temp_img.jpeg")

        return render_template("uploaded.html", file_path="img/temp_img.jpeg")


@app.route("/normal", methods=["POST"])
@nocache
def normal():
    return render_template("uploaded.html", file_path="img/temp_img.jpeg")


@app.route("/grayscale", methods=["POST"])
@nocache
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
    return render_template("uploaded.html", file_path="img/temp_img_grayscale.jpeg")


@app.route("/inverse", methods=["POST"])
@nocache
def inverse():
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
    return render_template("uploaded.html", file_path="img/temp_img_inverse.jpeg")


@app.route("/crop", methods=["POST"])
@nocache
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
    return render_template("uploaded.html", file_path="img/temp_img_crop.jpeg")


@app.route("/zoomin", methods=["POST"])
@nocache
def zoomin():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")

    img_arr = np.asarray(img)
    # img_arr.setflags(write=1)
    new_size = ((img_arr.shape[0] // 2),
                (img_arr.shape[1] // 2), img_arr.shape[2])
    new_arr = np.full(new_size, 255)
    # print(img_arr.shape, new_size)
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
    return render_template("uploaded.html", file_path="img/temp_img_zoomin.jpeg")


@app.route("/zoomout", methods=["POST"])
@nocache
def zoomout():
    zoominWithoutRender()
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
    return render_template("uploaded.html", file_path="img/temp_img_zoomout.jpeg")


def zoominWithoutRender():
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


@app.route("/fliphorizontal", methods=["POST"])
@nocache
def fliphorizontal():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")

    img_arr = np.asarray(img)

    flipped_arr = np.fliplr(img_arr)

    img_new = Image.fromarray(flipped_arr)
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_fliphorizontal.jpeg")
    return render_template("uploaded.html", file_path="img/temp_img_fliphorizontal.jpeg")


@app.route("/flipvertical", methods=["POST"])
@nocache
def flipvertical():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")

    img_arr = np.asarray(img)

    flipped_arr = np.flipud(img_arr)

    img_new = Image.fromarray(flipped_arr)
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_flipvertical.jpeg")
    return render_template("uploaded.html", file_path="img/temp_img_flipvertical.jpeg")


@app.route("/brightnesswithincrease", methods=["POST"])
@nocache
def brightnesswithincrease():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")
    img_arr = np.asfarray(img)

    val = request.form['val_increase']

    new_arr = img_arr + int(val)
    new_arr = np.clip(new_arr, 0, 255)

    img_new = Image.fromarray(new_arr.astype('uint8'))
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_brightnesswithincrease.jpeg")
    return render_template("brightness.html", file_path="img/temp_img_brightnesswithincrease.jpeg")


@app.route("/brightnesswithmultiply", methods=["POST"])
@nocache
def brightnesswithmultiply():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")

    img_arr = np.asfarray(img)
    val = request.form['val_multiply']
    new_arr = img_arr * int(val)
    new_arr = np.clip(new_arr, 0, 255)

    img_new = Image.fromarray(new_arr.astype('uint8'))
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_brightnesswithmultiply.jpeg")
    return render_template("brightness.html", file_path="img/temp_img_brightnesswithmultiply.jpeg")


@app.route("/darkeningwithdecrease", methods=["POST"])
@nocache
def darkeningwithdecrease():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")
    img_arr = np.asfarray(img)

    val = request.form['val_increase']
    new_arr = img_arr - int(val)
    new_arr = np.clip(new_arr, 0, 255)

    img_new = Image.fromarray(new_arr.astype('uint8'))
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_darkeningwithdecrease.jpeg")
    return render_template("darkening.html", file_path="img/temp_img_darkeningwithdecrease.jpeg")


@app.route("/darkeningwithdivide", methods=["POST"])
@nocache
def darkeningwithdivide():
    img = Image.open("static/img/temp_img.jpeg")
    img = img.convert("RGB")
    img_arr = np.asfarray(img)

    val = request.form['val_multiply']
    new_arr = img_arr // int(val)
    new_arr = np.clip(new_arr, 0, 255)

    img_new = Image.fromarray(new_arr.astype('uint8'))
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_darkeningwithdivide.jpeg")
    return render_template("darkening.html", file_path="img/temp_img_darkeningwithdivide.jpeg")


if __name__ == '__main__':
    app.run(debug=True)
