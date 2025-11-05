from flask import Flask, render_template

app = Flask(__name__)

#Rendering Templates !!
#Force reload on Chrome Shift + Reload
@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

