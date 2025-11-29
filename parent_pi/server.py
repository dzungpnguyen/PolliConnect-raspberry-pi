import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

USB_PATH = '/media/sda1'

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


@app.route('/data', methods=['GET'])
def fetch_data():
    try:
        # List all items in the USB root directory
        items = os.listdir(USB_PATH)
        
        # Filter to keep only directories
        folders = [item for item in items if os.path.isdir(os.path.join(USB_PATH, item))]
        
        return jsonify({
            "status": "success",
            "folders": folders
        })
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "USB drive not found"}), 404
    except PermissionError:
        return jsonify({"status": "error", "message": "Permission denied"}), 403
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
