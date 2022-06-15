from flask import Flask, render_template, request
import cdAI
import chatbot

def chatbot_response(query):
    # you can also use chatbot.getResponse(query) - this runs another model
    return cdAI.getResponse(query)


app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)


if __name__ == "__main__":
    app.run()
