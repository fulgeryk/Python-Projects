from flask import Flask
import random
app = Flask(__name__)

print (__name__)
print(random.__name__)

@app.route("/") # "/" -> home page
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/bye")
def say_bye():
    return "Bye"

if __name__ == "__main__":
    app.run()