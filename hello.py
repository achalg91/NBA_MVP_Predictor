from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def frontcourt():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route("/something")
def do_something():
    name = request.args.get("name", "World")
    return f'Hello, something!'

if __name__ == "__main__":
    app.run(debug=True)