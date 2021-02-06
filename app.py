from flask import Flask, render_template, request, redirect, url_for


application = Flask(__name__)

@application.route('/')
def hello_world():
    return "HighLevelAPI made by ПиФла"

@application.route('/get_scheme')
def ret_csheme():
    return redirect("http://192.168.0.109:3000/get_storage_scheme")




if __name__ == '__main__':
    application.run()
