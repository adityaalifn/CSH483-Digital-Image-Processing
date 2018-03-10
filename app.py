import numpy as np
from PIL import Image
import image_processing
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
    image_processing.grayscale()
    return render_template("uploaded.html", file_path="img/temp_img_grayscale.jpeg")


@app.route("/inverse", methods=["POST"])
@nocache
def inverse():
    image_processing.invers()
    return render_template("uploaded.html", file_path="img/temp_img_inverse.jpeg")


@app.route("/crop", methods=["POST"])
@nocache
def crop():
    image_processing.crop()
    return render_template("uploaded.html", file_path="img/temp_img_crop.jpeg")


@app.route("/zoomin", methods=["POST"])
@nocache
def zoomin():
    image_processing.zoomin()
    return render_template("uploaded.html", file_path="img/temp_img_zoomin.jpeg")


@app.route("/zoomout", methods=["POST"])
@nocache
def zoomout():
    image_processing.zoomout()
    return render_template("uploaded.html", file_path="img/temp_img_zoomout.jpeg")


@app.route("/fliphorizontal", methods=["POST"])
@nocache
def fliphorizontal():
    image_processing.fliphorizontal()
    return render_template("uploaded.html", file_path="img/temp_img_fliphorizontal.jpeg")


@app.route("/flipvertical", methods=["POST"])
@nocache
def flipvertical():
    image_processing.flipvertical()
    return render_template("uploaded.html", file_path="img/temp_img_flipvertical.jpeg")


@app.route("/brightnesswithincrease", methods=["POST"])
@nocache
def brightnesswithincrease():
    val = request.form['val_increase']
    image_processing.brightnesswithincrease(val)
    return render_template("brightness.html", file_path="img/temp_img_brightnesswithincrease.jpeg")


@app.route("/brightnesswithmultiply", methods=["POST"])
@nocache
def brightnesswithmultiply():
    val = request.form['val_multiply']
    image_processing.brightnesswithmultiply(val)
    return render_template("brightness.html", file_path="img/temp_img_brightnesswithmultiply.jpeg")


@app.route("/darkeningwithdecrease", methods=["POST"])
@nocache
def darkeningwithdecrease():
    val = request.form['val_increase']
    image_processing.darkeningwithdecrease(val)
    return render_template("darkening.html", file_path="img/temp_img_darkeningwithdecrease.jpeg")


@app.route("/darkeningwithdivide", methods=["POST"])
@nocache
def darkeningwithdivide():
    val = request.form['val_multiply']
    image_processing.darkeningwithdivide(val)
    return render_template("darkening.html", file_path="img/temp_img_darkeningwithdivide.jpeg")


@app.route("/convolution")
@nocache
def convolution():
    return render_template("convolution.html", file_path="img/temp_img.jpeg")


@app.route("/histogram")
@nocache
def histogram():
    image_processing.histogram()
    return render_template("histogram.html")


@app.route("/rotate90")
@nocache
def rotate90():
    image_processing.rotation90()
    return render_template("uploaded.html", file_path="img/temp_img_rotated.jpeg")


@app.route("/rotate180")
@nocache
def rotate180():
    image_processing.rotation180()
    return render_template("uploaded.html", file_path="img/temp_img_rotated.jpeg")


@app.route("/rotate270")
@nocache
def rotate270():
    image_processing.rotation270()
    return render_template("uploaded.html", file_path="img/temp_img_rotated.jpeg")


@app.route("/blurring")
@nocache
def blurring():
    blur_pix = 1 / 9
    image_processing.convolute(blur_pix, blur_pix, blur_pix,
                               blur_pix, blur_pix, blur_pix, blur_pix, blur_pix, blur_pix, "")
    return render_template("uploaded.html", file_path="img/temp_img_convolution.jpeg")


@app.route("/sharpening")
@nocache
def sharpening():
    image_processing.convolute(0, -1, 0, -1, 5, -1, 0, -1, 0, "")
    return render_template("uploaded.html", file_path="img/temp_img_convolution.jpeg")


@app.route("/edge_detection")
@nocache
def edge_detection():
    image_processing.convolute(-1, -1, -1, -1, 8, -1, -1, -1, -1, "edge")
    return render_template("uploaded.html", file_path="img/temp_img_convolution.jpeg")


@app.route("/convoluting", methods=["POST"])
@nocache
def convoluting():
    m11 = request.form['mat11']
    m12 = request.form['mat12']
    m13 = request.form['mat13']
    m21 = request.form['mat21']
    m22 = request.form['mat22']
    m23 = request.form['mat23']
    m31 = request.form['mat31']
    m32 = request.form['mat32']
    m33 = request.form['mat33']

    try:
        image_processing.convolute(
            m11, m12, m13, m21, m22, m23, m31, m32, m33, "")
    except:
        return render_template("convolution.html", file_path="img/temp_img.jpeg", alert="Matrix must filled all by integers")

    return render_template("convolution.html", file_path="img/temp_img_convolution.jpeg")


if __name__ == '__main__':
    app.run(debug=True)
