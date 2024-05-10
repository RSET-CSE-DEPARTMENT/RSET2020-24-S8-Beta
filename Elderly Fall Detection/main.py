import torch
import cv2
import math
import numpy as np
import os
from twilio.rest import Client

from torchvision import transforms
from utils.datasets import letterbox
from utils.general import non_max_suppression_kpt
from utils.plots import output_to_keypoint
from tqdm import tqdm

account_sid = 'sid_value'
auth_token = 'token'
client = Client(account_sid, auth_token)



def make_twilio_call():
    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to="phone_no.",
        from_="phone_no"
    )
    print("Twilio call SID:", call.sid)

def save_fall_video(frames, output_dir='fall_videos', fps=20.0):
    if not frames:
        print("No frames provided to save the video.")
        return
    
    # Create directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    output_path = os.path.join(output_dir, f"file_path")


    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()
    print(f"Fall video saved at {output_path}")


def fall_detection(poses):
    for pose in poses:
        xmin, ymin = (pose[2] - pose[4] / 2), (pose[3] - pose[5] / 2)
        xmax, ymax = (pose[2] + pose[4] / 2), (pose[3] + pose[5] / 2)
        left_shoulder_y = pose[23]
        left_shoulder_x = pose[22]
        right_shoulder_y = pose[26]
        left_body_y = pose[41]
        left_body_x = pose[40]
        right_body_y = pose[44]
        len_factor = math.sqrt(((left_shoulder_y - left_body_y) ** 2 + (left_shoulder_x - left_body_x) ** 2))
        left_foot_y = pose[53]
        right_foot_y = pose[56]
        dx = int(xmax) - int(xmin)
        dy = int(ymax) - int(ymin)
        difference = dy - dx
        if left_shoulder_y > left_foot_y - len_factor and left_body_y > left_foot_y - (len_factor / 2) and left_shoulder_y > left_body_y - (len_factor / 2) or (right_shoulder_y > right_foot_y - len_factor and right_body_y > right_foot_y - (len_factor / 2) and right_shoulder_y > right_body_y - (len_factor / 2)) or difference < 0:
            return True, (xmin, ymin, xmax, ymax)
    return False, None

def falling_alarm(image, bbox):
    x_min, y_min, x_max, y_max = bbox
    cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color=(0, 0, 255),
                  thickness=5, lineType=cv2.LINE_AA)
    cv2.putText(image, 'Person Fell down', (11, 100), 0, 1, [0, 0, 255], thickness=3, lineType=cv2.LINE_AA)

def get_pose_model():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("device: ", device)
    weights = torch.load('yolov7-w6-pose.pt', map_location=device)
    model = weights['model']
    _ = model.float().eval()
    if torch.cuda.is_available():
        model = model.half().to(device)
    return model, device

def get_pose(image, model, device):
    image = letterbox(image, 960, stride=64, auto=True)[0]
    image = transforms.ToTensor()(image)
    image = torch.tensor(np.array([image.numpy()]))
    if torch.cuda.is_available():
        image = image.half().to(device)
    with torch.no_grad():
        output, _ = model(image)
    output = non_max_suppression_kpt(output, 0.25, 0.65, nc=model.yaml['nc'], nkpt=model.yaml['nkpt'],
                                     kpt_label=True)
    with torch.no_grad():
        output = output_to_keypoint(output)
    return image, output

def prepare_image(image):
    _image = image[0].permute(1, 2, 0) * 255
    _image = _image.cpu().numpy().astype(np.uint8)
    _image = cv2.cvtColor(_image, cv2.COLOR_RGB2BGR)
    return _image

def process_webcam():
    model, device = get_pose_model()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error opening video stream or file")
        return

    fall_detected = False
    fall_frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting...")
            break

        image, output = get_pose(frame, model, device)
        _image = prepare_image(image)
        is_fall, bbox = fall_detection(output)
        if is_fall:
            if not fall_detected:
                fall_detected = True
                make_twilio_call()
            falling_alarm(_image, bbox)
            fall_frames.append(_image)
        elif fall_detected:
            # Fall event ended
            fall_detected = False
            save_fall_video(fall_frames)
            fall_frames = []

        cv2.imshow('frame', _image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    process_webcam()
