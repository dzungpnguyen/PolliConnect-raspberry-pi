from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("home.html")


@app.route('/devices')
def get_nearby_devices():
    devices = [
        {"id": 1, "name": "PolliCam1", "device_id": 5},
        {"id": 2, "name": "PolliCam2", "device_id": 12},
        {"id": 3, "name": "PartnerCam", "device_id": 20}
    ]
    return devices

if __name__ == '__main__':
    app.run(debug=True)
