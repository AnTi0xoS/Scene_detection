import ffmpeg


def detect_scene_changes(video_path):
    video_info = ffmpeg.probe(video_path)['streams']
    video_stream = next((stream for stream in video_info if stream['codec_type'] == 'video'), None)
    duration = float(video_stream['duration'])

    output = ffmpeg.input(video_path).output('null', vf='select=gt(scene,0.4)', f='null', **{'loglevel': 'panic'})
    ffmpeg.run(output)

    scene_changes = []
    with open('ffmpeg.log') as f:
        for line in f:
            if 'Parsed_showinfo_0 @ ' in line:
                scene_changes.append(float(line.split('n:')[-1].strip()))

    scene_changes = [round(change / duration, 2) for change in scene_changes]
    return scene_changes


video_file = "BigBuckBunny.mp4"
scene_changes = detect_scene_changes(video_file)
print("Scene changes at timecodes:", scene_changes)