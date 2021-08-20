import ZadarmaApi
from flask import Flask, render_template
import json

app = Flask(__name__)

z_api = ZadarmaApi.API(key='6185183df698948157f3',
                       secret='8f7483a2a108dd4e4d8a')


def getWebrtcKey():
    data = z_api.call('/v1/webrtc/get_key/', params={"sip": "261318-112"})
    data = json.loads(data)
    key = data["key"]
    return key


@app.route('/')
def hello_world():
    return render_template("index.html", webrtcKey=getWebrtcKey(), login="261318-112")


if __name__ == '__main__':
    app.run(debug=True)

    # get tariff information
    # print(z_api.call('/v1/tariff/'))
    # set callerid for your sip number
