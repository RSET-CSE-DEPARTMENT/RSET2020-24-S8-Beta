import subprocess

# Define the commands to be executed
commands = [
    
    "pip install -r requirements.txt",
    "pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118",
    "python detect.py --weights yolov7-custom.pt --conf 0.5 --img-size 640 --source 0 --view-img --no-trace"
]

# Execute each command
for cmd in commands:
    subprocess.run(cmd, shell=True)
