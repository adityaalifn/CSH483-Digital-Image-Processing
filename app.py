import numpy as np
from PIL import Image
import os
from flask import Flask, render_template, request
import cv2

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/index")
@app.route("/")
def index():
    return render_template("home.html", file_path="img/image_here.jpg")


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
            return render_template("home.html", file_path="img/no_image_selected.gif")

        filename = "temp_img." + file.filename.split(".")[-1]
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

        return render_template("uploaded.html", file_path="img/" + filename)

@app.route("/grayscale", methods=["POST"])
def grayscale():
    img = Image.open("static/img/temp_img.png")

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

    img = Image.fromarray(arr_gray)
    img.show()
    return render_template("uploaded.html")


if __name__ == '__main__':
    app.run(debug=True)
