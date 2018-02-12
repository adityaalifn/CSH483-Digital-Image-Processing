import numpy as np
from PIL import Image
import os
from flask import Flask, render_template, request
import random

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/index")
@app.route("/")
def index():
    return render_template("home.html", file_path="img/image_here.jpg")

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
def about():
    return render_template("about.html")


@app.route("/upload", methods=["POST"])
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
def normal():
    return render_template("uploaded.html", file_path="img/temp_img.jpeg")


@app.route("/grayscale", methods=["POST"])
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
    # print(r, r*0.5)

    if sum_r > sum_g and sum_r > sum_b:
        arr_gray = (0.5 * r) + (0.25 * g) + (0.25 * b)
    elif sum_g > sum_r and sum_g > sum_b:
        arr_gray = (0.25 * r) + (0.5 * g) + (0.25 * b)
    else:
        arr_gray = (0.25 * r) + (0.25 * g) + (0.5 * b)

    img_new = Image.fromarray(arr_gray)
    img_new = img_new.convert("RGB")
    img_new.save("static/img/temp_img_grayscale.jpeg")
    return render_template("uploaded.html", file_path="img/temp_img_grayscale.jpeg")


@app.route("/inverse", methods=["POST"])
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
    print("A")
    return render_template("uploaded.html", file_path="img/temp_img_inverse.jpeg")


if __name__ == '__main__':
    app.run()
