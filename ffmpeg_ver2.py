import ffmpeg
import math

def timecode_to_seconds(timecode):
    time_parts = timecode.split(':')
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(time_parts[2])
    return hours * 3600 + minutes * 60 + seconds


def seconds_to_timecode(seconds):
    hours = math.floor(seconds / 3600)
    minutes = math.floor((seconds % 3600) / 60)
    seconds = seconds % 60
    return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)


def detect_scene_change(video_path):
    probe = ffmpeg.probe(video_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if video_stream is None:
        raise Exception('Не удалось найти видео поток.')

    width = int(video_stream['width'])
    height = int(video_stream['height'])
    frame_rate = eval(video_stream['avg_frame_rate'])
    frame_duration = 1 / frame_rate

    scene_changes = []
    previous_frame = None
    current_frame_number = 0

    ffmpeg.input(video_path).output('temp/frame%d.jpg', vf='select=eq(n\,{}),scale={}:{}'.format(current_frame_number, width, height)).run()
    current_frame_number += 1
    previous_frame = ffmpeg.input('temp/frame{}.jpg'.format(current_frame_number - 1))

    while True:
        ffmpeg.input(video_path).output('temp/frame%d.jpg', vf='select=eq(n\,{}),scale={}:{}'.format(current_frame_number, width, height)).run()
        current_frame = ffmpeg.input('temp/frame{}.jpg'.format(current_frame_number))
        ssim_filter = ffmpeg.filter([previous_frame, current_frame], 'ssim', stats_file='stats_file.txt')
        ffmpeg.output(ssim_filter, 'stats_file.txt').run()

        with open('stats_file.txt', 'r') as f:
            ssim_line = f.readline()
            ssim_value = float(ssim_line.split(' ')[1])

        if ssim_value < 0.9:
            start_time = current_frame_number * frame_duration
            scene_changes.append(seconds_to_timecode(start_time))
        else:
            break

        previous_frame = current_frame
        current_frame_number += 1

    return scene_changes


video_file = "BigBuckBunny.mp4"
scene_changes = detect_scene_change(video_file)
print(scene_changes)