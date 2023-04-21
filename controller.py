# GUI

import RPi.GPIO as GPIO
import time
import os

makerobo_RelayPin=11 


from flask import Flask,render_template,render_template_string
app=Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jLwf/T'

from flask import request,session,redirect

dt=0
sleepdt=10000

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(makerobo_RelayPin, GPIO.OUT)
    GPIO.output(makerobo_RelayPin, GPIO.LOW)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/s")
def s():
    page = '''
    <form action="{{ url_for('do_submit') }}" method="post">
        <p>
            Please input your HTS time: <input type="text" name="HTStime" />
        </p>
    <input type="submit" value="Submit" />
    </form>
    '''
    return render_template_string(page)

@app.route('/do_submit', methods=['POST'])
def do_submit():
    name = request.form.get('HTStime')
    session['HTStime']=name
    dt=session.get('HTStime')
    with open("test.txt","w") as f:
        f.write(dt) 
    return 'Update Setting Success!'

@app.route('/clear')
def clear():
    session.pop('HTStime', None)
    return redirect(url_for('submit_value'))

@app.route('/show')
def show():
    return session['HTStime']

@app.route("/on")
def on():
    with open('./test.txt', 'r') as f:
        HTS_time = f.read()
    dt = HTS_time.split()[0]
    GPIO.output(makerobo_RelayPin,GPIO.HIGH)
    time.sleep(float(dt))
    GPIO.output(makerobo_RelayPin,GPIO.LOW)
#    time.sleep(100000)
#    os.remove("./time.txt")
    return render_template("main.html")


if __name__ == "__main__":
    setup()
    app.run(host="0.0.0.0", port=19258, debug=True)
