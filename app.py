import os
from flask import Flask, render_template, request

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

        return render_template("home.html", file_path="img/" + filename)


if __name__ == '__main__':
    app.run(debug=True)
