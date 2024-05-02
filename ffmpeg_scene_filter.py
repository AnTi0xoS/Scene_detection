import ffmpeg
import re


def detect_scene_changes(video_path):
    input_stream = ffmpeg.input(video_path)
    output_stream = (
        input_stream
        .filter('select', 'gte(scene,0.001)')
        .filter('showinfo')
        .output('dummy.mp4', format='null')
    )
    stdout, stderr = ffmpeg.run(output_stream, capture_stdout=True, capture_stderr=True)
    output = stderr.decode('utf-8')
    scene_changes = []
    for line in output.split('\n'):
        match = re.search(r'pts_time:([\d.]+)', line)
        if match:
            scene_changes.append(float(match.group(1)))
    return scene_changes


if __name__ == "__main__":
    video_path = 'four_cars_night.mp4'
    changes = detect_scene_changes(video_path)
    print("Scene Changes:")
    for scene_num in range(len(changes)):
        print(f"Scene {scene_num}:", changes[scene_num])
