import os
from pathlib import Path
from flask import Flask, render_template, jsonify, send_from_directory

app = Flask(__name__)

# USB_PATH = Path('/media/sda1')
USB_PATH = Path('/home/lacnguyen/PEANUT/GIT/PolliConnect-Raspberry-Pi/test_usb_drive')

# List of image extensions to look for
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')


@app.route('/')
def hello():
    return render_template("home.html")


@app.route('/data', methods=['GET'])
def fetch_data():
    try:
        # List directories in the USB
        if not USB_PATH.exists():
            return jsonify({"status": "error", "message": "USB drive not found"}), 404
        
        folders = [f.name for f in USB_PATH.iterdir() if f.is_dir()]

        return render_template("data.html", folders=folders)

    except PermissionError:
        return jsonify({"status": "error", "message": "Permission denied"}), 403
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# function to retrieve all devices connected to the Pi's network (maybe exclude non-raspberry-pi because they don't have unique ID aka serial number)
@app.route('/devices')
def get_nearby_devices():
    devices = [
        {"serial": "parent_pi", "ip": "192.168.4.1", "mac": "dc:a6:32:7b:19:f0", "hostname": "pi1", "source": "dhcp"},
        {"serial": "10000000abcd1234", "ip": "192.168.4.1", "mac": "dc:a6:32:7b:19:f0", "hostname": "pi1", "source": "dhcp"},
        {"serial": "20000000abcd1234", "ip": "192.168.4.2", "mac": "dc:a6:32:7b:19:f0", "hostname": "pi2", "source": "dhcp"},
        {"serial": "30000000abcd1234", "ip": "192.168.4.3", "mac": "dc:a6:32:7b:19:f0", "hostname": "pi3", "source": "dhcp"},
    ]
    return devices


@app.route('/data/<device_serial>', methods=['GET'])
def get_device_data(device_serial):
    device_folder = USB_PATH / device_serial

    if not device_folder.exists():
        return jsonify({"status": "error", "message": f"Device {device_serial} not found"}), 404
    if not device_folder.is_dir():
        return jsonify({"status": "error", "message": f"{device_serial} is not a folder"}), 400

    try:
        # List image files
        files = [f.name for f in device_folder.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]
        return render_template("device_data.html", device_serial=device_serial, files=files)

    except PermissionError:
        return jsonify({"status": "error", "message": "Permission denied"}), 403
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

# Route to serve individual files from the device folder
@app.route('/data/<device_serial>/<filename>')
def serve_file(device_serial, filename):
    device_folder = USB_PATH / device_serial
    return send_from_directory(directory=device_folder, path=filename)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
