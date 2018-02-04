from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html", file_path = "D:\\!Telkom University\\Pemrosesan Citra Digital\\Tugas\\CSH483-Digital-Image-Processing\\templates\\img\\image_here.jpg")

@app.route("/preview", methods=["POST"])
def preview():
    image_path = request.form["image_path"]
    return render_template("home.html", file_path = image_path)
    

if __name__ == "__main__":
    app.run(debug=True)
