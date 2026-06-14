from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

HTML_PAGE = """
<!doctype html>

<title>AI Annotation Tool</title>

<h1>Upload Image with Label</h1>

<form method=post enctype=multipart/form-data>

  <input type=file name=file>

  <br><br>

  <input type=text name=label placeholder="Enter Label">

  <br><br>

  <input type=submit value=Upload>

</form>

{% if filename %}

    <h2>Uploaded Image:</h2>

    <img src="/uploads/{{ filename }}" width="300">

    <h3>Label:</h3>

    <p>{{ label }}</p>

{% endif %}

<p>{{ message }}</p>
"""

@app.route("/", methods=["GET", "POST"])

def upload_file():

    message = ""
    filename = ""
    label = ""

    if request.method == "POST":

        file = request.files["file"]

        label = request.form["label"]

        if file.filename != "":

            filepath = os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )

            file.save(filepath)

            filename = file.filename

            message = "Image and label uploaded successfully!"

    return render_template_string(
        HTML_PAGE,
        message=message,
        filename=filename,
        label=label
    )

@app.route("/uploads/<filename>")

def uploaded_file(filename):

    return app.send_static_file(
        os.path.join(UPLOAD_FOLDER, filename)
    )

app.static_folder = "."

if __name__ == "__main__":

    app.run(debug=True)