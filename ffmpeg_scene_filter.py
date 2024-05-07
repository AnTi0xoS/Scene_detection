import ffmpeg
import re
import time
import psutil


def detect_scene_changes_ffmpeg(path):
    input_stream = ffmpeg.input(path)
    output_stream = (
        input_stream
        .filter('select', 'gte(scene,0.001)')
        .filter('showinfo')
        .output('dummy.mp4', format='null')
    )
    start_time = time.time()
    cpu_usage_before = psutil.cpu_percent(interval=None)
    stdout, stderr = ffmpeg.run(output_stream, capture_stdout=True, capture_stderr=True)
    end_time = time.time()
    cpu_usage_after = psutil.cpu_percent(interval=None)
    output = stderr.decode('utf-8')
    scene_changes = []
    for line in output.split('\n'):
        match = re.search(r'pts_time:([\d.]+)', line)
        if match:
            scene_changes.append(float(match.group(1)))
    fps = len(scene_changes) / (end_time - start_time)
    memory = psutil.Process().memory_info().rss / 1024 / 1024
    return scene_changes, end_time - start_time, memory, cpu_usage_after - cpu_usage_before, fps


if __name__ == "__main__":
    video_path = 'four_cars_night.mp4'
    changes, execution_time, memory_usage, cpu_usage, fps = detect_scene_changes_ffmpeg(video_path)
    print("Scene Changes:")
    for scene_num in range(len(changes)):
        print(f"Scene {scene_num}:", changes[scene_num])
    print("\n--- ffmpeg_scene_filter ---")
    print("Execution Time:", execution_time, "seconds")
    print("FPS:", fps)
    print("Memory Usage:", memory_usage, "MB")
    print("CPU Usage:", cpu_usage, "%")