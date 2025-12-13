from pathlib import Path
from flask import Blueprint, request, render_template, jsonify, send_from_directory, current_app


# List of image extensions to look for
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')


master_bp = Blueprint('master', __name__)

# MASTER_DATA_FOLDER = None

# @master_bp.record
# def record_params(setup_state):
#     global MASTER_DATA_FOLDER
#     current_app = setup_state.app
#     MASTER_DATA_FOLDER = Path(current_app.config["MASTER_DATA_FOLDER"])

"""Initialize blueprint config from app config"""
def init_master_bp(app):
    master_bp.DEBUG = app.config["DEBUG"]
    master_bp.MASTER_DATA_FOLDER = Path(app.config["MASTER_DATA_FOLDER"])


def get_connected_devices():
    devices = [
        {"serial": "parent_pi", "ip": "192.168.4.1", "mac": "dc:a6:32:7b:19:f0", "hostname": "pi1", "source": "dhcp"},
        {"serial": "10000000abcd1234", "ip": "192.168.4.1", "mac": "dc:a6:32:7b:19:f0", "hostname": "pi1", "source": "dhcp"},
    ]
    return devices

"""
Read and show the specifications of the master camera
Input: None
Output:
Note: This is example data, the developped function should detect automatically camera specs. To be consistent and coherent, data shoudle be stored in master_bp.<data-name>
"""
@master_bp.route("/master-camera")
def show_master_info(): 
    master_ip = None
    return render_template("master_camera.html", master_ip=master_ip)


# function to retrieve all devices connected to the Pi's network (should exclude non-raspberry-pi devices because they don't have unique ID aka serial number)
@master_bp.route('/devices')
def show_connected_devices():
    devices = get_connected_devices()
    return devices


@master_bp.route('/')
def hello():
    return render_template("home.html")


@master_bp.route('/data', methods=['GET'])
def fetch_data():
    try:
        # List directories in the USB
        if not master_bp.MASTER_DATA_FOLDER.exists():
            return jsonify({"status": "error", "message": "USB drive not found"}), 404
        
        device_ids = [folder.name for folder in master_bp.MASTER_DATA_FOLDER.iterdir() if folder.is_dir()]

        return render_template("data.html", device_ids=device_ids)

    except PermissionError:
        return jsonify({"status": "error", "message": "Permission denied"}), 403
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@master_bp.route('/data/<device_id>', methods=['GET'])
def get_device_data(device_id):
    device_folder = master_bp.MASTER_DATA_FOLDER / device_id

    if not device_folder.exists():
        return jsonify({"status": "error", "message": f"Device {device_id} not found"}), 404
    if not device_folder.is_dir():
        return jsonify({"status": "error", "message": f"{device_id} is not a folder"}), 400

    try:
        # List image files (limit to 10 during DEBUG)
        files = [f.name for f in device_folder.iterdir() if f.is_file() and f.suffix.lower() in image_extensions][:10]
        return render_template("device_data.html", device_id=device_id, files=files)

    except PermissionError:
        return jsonify({"status": "error", "message": "Permission denied"}), 403
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

# Route to serve individual files from the device folder
@master_bp.route('/data/<device_id>/<filename>')
def serve_file(device_id, filename):
    device_folder = master_bp.MASTER_DATA_FOLDER / device_id
    return send_from_directory(directory=device_folder, path=filename)


# Receive files from child devices and save them in device-specific folders
@master_bp.route('/upload/<device_id>', methods=['POST'])
def upload_file(device_id):
    device_folder = master_bp.MASTER_DATA_FOLDER / device_id
    device_folder.mkdir(parents=True, exist_ok=True)  # create folder if it doesn't exist

    if 'files' not in request.files:
        return jsonify({"error": "No files part in the request"}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    saved_files = []
    for f in files:
        save_path = device_folder / f.filename
        f.save(save_path)
        saved_files.append(str(save_path))

    return jsonify({"message": f"Saved {len(saved_files)} files", "files": saved_files}), 200
