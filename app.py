import os
from flask import Flask, render_template, request

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("home.html", file_path="img/image_here_123123123.jpg")


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, "static/img")
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        if filename == "":
            return render_template("home.html", file_path="img/no-image-selected-123123123.gif")
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    return render_template("home.html", file_path="img/"+filename)


if __name__ == '__main__':
    app.run(debug=True)
