import ffmpeg
import re
import time
import psutil


def detect_scene_changes(path):
    input_stream = ffmpeg.input(path)
    output_stream = (
        input_stream
        .filter('select', 'gte(scene,0.001)')
        .filter('showinfo')
        .output('dummy.mp4', format='null', codec='libx264')
    )
    start_time_total = time.time()
    cpu_usage_before = psutil.cpu_percent(interval=None)

    start_time_decode = time.time()
    stdout, stderr = ffmpeg.run(output_stream, capture_stdout=True, capture_stderr=True)
    end_time_decode = time.time()
    decode_time = end_time_decode - start_time_decode

    start_time_recognition = time.time()
    output = stderr.decode('utf-8')
    scene_changes = []
    for line in output.split('\n'):
        match = re.search(r'pts_time:([\d.]+)', line)
        if match:
            scene_changes.append(float(match.group(1)))
    end_time_recognition = time.time()
    recognition_time = end_time_recognition - start_time_recognition

    end_time_total = time.time()
    cpu_usage_after = psutil.cpu_percent(interval=None)

    execution_time = end_time_total - start_time_total
    fps = len(scene_changes) / execution_time
    memory = psutil.Process().memory_info().rss / 1024 / 1024

    return scene_changes, execution_time, decode_time, recognition_time, memory, cpu_usage_after - cpu_usage_before, fps


if __name__ == "__main__":
    video_path = 'video_files/1_four_cars_night.mp4'
    # for 1_four_cars_night.mp4
    # Scene 1 - 9.66
    # Scene 2 - 15.97
    # Scene 3 - 19.58
    changes, execution_time, decode_time, recognition_time, memory_usage, cpu_usage, fps = detect_scene_changes(
        video_path)
    print("Scene Changes:")
    for scene_num in range(len(changes)):
        print(f"Scene {scene_num}:", changes[scene_num])
    print("\n--- ffmpeg_scene_filter ---")
    print("Execution Time:", execution_time, "seconds")
    print("Decode Time:", decode_time, "seconds")
    print("Recognition Time:", recognition_time, "seconds")
    print("FPS:", fps)
    print("Memory Usage:", memory_usage, "MB")
    print("CPU Usage:", cpu_usage, "%")
