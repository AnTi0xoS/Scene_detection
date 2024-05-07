import cv2
import time
import psutil


def detect_scene_change(frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)
    mean_diff = diff.mean()
    return mean_diff > 1.35


def detect_scene_changes_cv2(video_file):
    cap = cv2.VideoCapture(video_file)
    ret, prev_frame = cap.read()
    if not ret:
        print("Error: Could not read the video file.")
        return []
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    scene_changes = []

    start_time = time.time()
    cpu_usage_before = psutil.cpu_percent(interval=None)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if detect_scene_change(prev_gray, gray):
            scene_changes.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
        prev_gray = gray
    cap.release()
    end_time = time.time()
    cpu_usage_after = psutil.cpu_percent(interval=None)
    fps = len(scene_changes) / (end_time - start_time)
    memory = psutil.Process().memory_info().rss / 1024 / 1024
    return scene_changes, end_time - start_time, memory, cpu_usage_after - cpu_usage_before, fps


if __name__ == "__main__":
    video_path = "four_cars_night.mp4"
    scene_changes, execution_time, memory_usage, cpu_usage, fps = detect_scene_changes_cv2(video_path)
    print("Scene Changes:")
    for scene_num, scene_time in enumerate(scene_changes):
        print(f"Scene {scene_num}:", scene_time)
    print("\n--- cv2_scene_filter ---")
    print("Execution Time:", execution_time, "seconds")
    print("FPS:", fps)
    print("Memory Usage:", memory_usage, "MB")
    print("CPU Usage:", cpu_usage, "%")
