import ffmpeg


def detect_scene_changes(video_file):
    input_args = {'r': 1, 'f': 'image2pipe', 'vcodec': 'mjpeg'}
    output_args = "-vf select='gt(scene,0.4)' -f null"

    scene_changes = []
    try:
        output = ffmpeg.input(video_file, **input_args).output('dummy', output_args).run(capture_stdout=True, capture_stderr=True)
        scene_output = output.stderr.decode()
        for line in scene_output.split("n"):
            if "pts_time:" in line:
                timecode = line.split("pts_time:")[1].split()[0]
                scene_changes.append(float(timecode))

    except ffmpeg._run.Error as e:
        print(f'An error occurred while running ffmpeg: {e.stderr.decode()}')

    return scene_changes


video_file = 'BigBuckBunny.mp4'
scene_changes = detect_scene_changes(video_file)
for timecode in scene_changes:
    print(f'Scene change at timecode: {timecode}')
