import ZadarmaApi
from flask import Flask, session, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = 'asdsdfsdfs13sdf_df%&'

z_api = ZadarmaApi.API(key='6185183df698948157f3',
                       secret='8f7483a2a108dd4e4d8a')


def getWebrtcKey(sip):
    data = z_api.call('/v1/webrtc/get_key/', params={"sip": sip})
    data = json.loads(data)
    key = data["key"]
    return key


def getPbxInfo(sip):
    data = z_api.call(f'/v1/pbx/internal/{sip}/info/')
    return data


@app.route('/login', methods=['GET', 'POST'])
def login():
    if(session.get('login')):
        flash('You are Already logged in', "info")
        session["notify"] = {
            "message": "You are Already logged in", "category": "success"}
        return redirect(url_for('index'))
    if request.method == 'POST':
        session['sip'] = request.form['sip']
        password = request.form['password']
        sip = session['sip']
        if("-" in sip and password == "Siebel12!s"):
            userInfo = json.loads(getPbxInfo(sip.split("-")[1]))
            if(userInfo['status'] == "success"):
                session['sip'] = request.form['sip']
                session['login'] = True

                return redirect(url_for('index'))
        else:
            session["notify"] = {
                "message": "Login credentials are invalid", "category": "danger"}
            # return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    if(session.get('login') == None):
        session["notify"] = {
            "message": "You are Already logged Out", "category": "danger"}
        return redirect(url_for('login'))

    session.pop('sip', None)
    session.pop('login', None)
    session["notify"] = {
        "message": "Successfully logged Out", "category": "success"}
    return redirect(url_for('login'))


@app.route('/')
def index():
    if(session.get('login') == None):
        session["notify"] = {
            "message": "Please Log in to continue", "category": "danger"}
        return redirect(url_for('login'))
    sip = session['sip']
    key = getWebrtcKey(sip)
    userInfo = json.loads(getPbxInfo(sip.split("-")[1]))
    session["notify"] = {
        "message": "You are successfully logged in", "category": "success"}
    print(userInfo)
    return render_template("index.html", webrtcKey=key, login=sip, userInfo=userInfo)


if __name__ == '__main__':
    app.run(debug=True)

    # get tariff information
    # print(z_api.call('/v1/tariff/'))
    # set callerid for your sip number
