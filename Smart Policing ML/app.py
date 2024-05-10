from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Mock user
mock_user = {
    'username': 'user',
    'password': 'password'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == mock_user['username'] and password == mock_user['password']:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return 'Login Failed!'
    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
     
         if not session.get('logged_in'):
             return redirect(url_for('login'))
         if request.method == 'GET' or request.method == 'POST':
             if 'logout' in request.form:
                 return redirect(url_for('login'))
         return render_template('index.html')
@app.route('/fire_detection_script', methods=['POST'])
def fire_detection_script():
    # Code for fire detection
    try:
        
        import subprocess
        import os
        import time
         # Install necessary packages
        subprocess.run(['pip', 'install', '--upgrade', 'opencv-python'])
        subprocess.run(['pip', 'install', 'keyboard'])
         # Change working directory to the YOLOv5 repository
        os.chdir('yolov7-custom')

         # Install YOLOv5 requirements
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

         #  Print current working directory
        print(os.getcwd())

        
         # Start YOLOv5 detection in a separate process
        #process = subprocess.Popen(['python', 'detect.py', '--weights', 'best.pt', '--conf', '0.35', '--img-size', '640', '--source', 'https://192.168.100.78:4343/video', '--view-img'])
        #process = subprocess.Popen(['python', 'detect.py', '--weights', 'best.pt', '--conf', '0.35', '--img-size', '640', '--source', 'https://192.168.168.9:4343/video', '--view-img'])
        process = subprocess.Popen(['python', 'detect.py', '--weights', 'best.pt', '--conf', '0.35', '--img-size', '640', '--source', '0', '--view-img'])
        main_command = ['python', 'main.py']
        process_main = subprocess.Popen(main_command)
        return 'Detection started'
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
