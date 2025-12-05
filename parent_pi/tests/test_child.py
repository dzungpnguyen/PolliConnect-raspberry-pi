import requests
from pathlib import Path

PARENT_PI_IP = "192.168.1.45"
DEVICE_ID = "dung_computer"
UPLOAD_URL = f"http://{PARENT_PI_IP}:5000/upload/{DEVICE_ID}"

def send_files(list_filepaths):
    files = []

    for filepath in list_filepaths:
        filepath = Path(filepath)
        if filepath.exists():
            files.append(('files', (filepath.name, open(filepath, 'rb'))))
        else:
            print(f"File not found: {filepath}")

    if not files:
        print("No valid files to upload.")
        return

    response = requests.post(UPLOAD_URL, files=files)

    try:
        print("Server response:", response.json())
    except:
        print("Raw server response:", response.text)


if __name__ == "__main__":
    # Test
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    child_folder = Path("/home/lacnguyen/PEANUT/GIT/PolliConnect-Raspberry-Pi/usb_child")
    files_to_send = [f for f in child_folder.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]

    send_files(files_to_send)
