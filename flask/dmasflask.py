from pathlib import Path
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify,send_file)
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
import test_make_sim
import os


app = Flask(__name__)
CORS(app)

@app.route('/show')
def show_register():
    """Show registration form"""

    return render_template("index.html")

#rendering the HTML page which has the button
@app.route('/traffic_sim')
def json():
    return render_template('json.html')

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    answer={}
    #os.remove("/home/dmas/marouf/flask/low_manhattan_sim/low_manhattan_flow.json")
    answer=test_make_sim.main()
    return render_template('result.html', result=answer)
@app.route('/downloadreplayjson')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "/home/dmas/marouf/flask/low_manhattan_sim/replay_roadnet.json"
    return send_file(path, as_attachment=True)
@app.route('/downloadreplaytxt')
def downloadFile2 ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "/home/dmas/marouf/flask/low_manhattan_sim/replay.txt"
    return send_file(path, as_attachment=True)
if __name__ == "__main__":
    # Change app.debug to False before launch
    # Use the DebugToolbar
    app.run(host='0.0.0.0', port='6969',debug = True)
    DebugToolbarExtension(app)
