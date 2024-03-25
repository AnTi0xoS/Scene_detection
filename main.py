import cv2
import subprocess
import os


def extract_frames(video_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    command = ['ffmpeg', '-i', video_file, '-vf', 'fps=1', f'{output_dir}/frame_%05d.jpg']
    subprocess.call(command)


def detect_scene_change(frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)
    mean_diff = diff.mean()
    return mean_diff > 20


def find_scene_changes(video_file):
    cap = cv2.VideoCapture(video_file)
    ret, prev_frame = cap.read()
    if not ret:
        print("Error: Could not read the video file.")
        return []

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    scene_changes = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if detect_scene_change(prev_gray, gray):
            scene_changes.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)

        prev_gray = gray

    cap.release()
    return scene_changes


if __name__ == "__main__":
    video_file = "four_cars_night.mp4"
    output_dir = "frames"
    extract_frames(video_file, output_dir)
    scene_changes = find_scene_changes(video_file)
    print("Scene changes (in seconds):", scene_changes)
