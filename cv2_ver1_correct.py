import cv2


def detect_scene_changes(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"Could not open video file: {path}")
        return []

    scene_detect = []
    frame_count = 0
    prev_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_frame is None:
            prev_frame = gray
            continue

        frame_diff = cv2.absdiff(prev_frame, gray)
        diff_mean = frame_diff.mean()
        if diff_mean > 40:
            current_timecode = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            scene_detect.append(current_timecode)
        prev_frame = gray
        frame_count += 1

    cap.release()
    return scene_detect


video_file = 'BigBuckBunny.mp4'
scene_changes = detect_scene_changes(video_file)
for timecode in scene_changes:
    print(f'Scene change at timecode: {timecode} seconds')
