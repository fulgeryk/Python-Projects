from flask import Flask, render_template
import requests
posts = requests.get(url="https://api.npoint.io/674f5423f73deab1e9a7").json()

app = Flask(__name__)

@app.route('/')
def get_index():
    return render_template('index.html', header_image="assets/img/home-bg.jpg", all_posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", header_image="assets/img/about-bg.jpg")

@app.route("/contact")
def contact():
    return render_template("contact.html", header_image="assets/img/contact-bg.jpg")


if __name__ == "__main__":
    app.run(debug=True)