import os
import json
import shutil
import moviepy.editor as mp
from audio_processing import transcribe_large_audio
from text_processing import read_text_from_video

dir = os.path.dirname(os.path.dirname(__file__))

video_mapping = {
    '1': 'pt-BR',
    # '2': 'pt-BR',
    '3': 'en-US',
    # '4': 'pt-BR',
    # '5': 'es-ES',
    # '6': 'pt-BR',
    # '7': 'es-ES',
    # '8': 'pt-BR',
    # '9': 'ar',
    # '10': 'pt-BR',
    # '11': 'pt-BR',
    # '12': 'pt-BR'
}

data = []
chunks_folder = 'audio-chunks'
thumbnails_folder = 'thumbnails'
videos_folder = 'videos-test'
audio_temp_path = f'audio-chunks/temp_audio.wav'
data_filename = 'data-test.json'

def save_thumbnail(video, video_name):
    if not os.path.isdir(thumbnails_folder):
        os.mkdir(thumbnails_folder)

    output_path = os.path.join(dir, f"{thumbnails_folder}/", f"thumbnail_{video_name}.png")
    video.save_frame(output_path, t=1)
    return output_path

def process_videos():
    for video_name in video_mapping.keys():
        print("Starting recognition of video {}".format(video_name))
        video_path = os.path.join(dir, f"{videos_folder}", video_name+'.mp4')
        
        if not os.path.isdir(chunks_folder):
            os.mkdir(chunks_folder)

        video = mp.VideoFileClip(video_path, verbose=False)
        duration = video.duration

        video_data = {
            "video": video_name+'.mp4',
            "fps": video.fps,
            "dimensions": video.size,
            "duration": f"{int(duration // 60):02d}:{int(duration % 60):02d}",
            "language": video_mapping[video_name],
            "thumbnail": "",
            "keywords": []
        }

        print("---> Text in video being processed...")
        textual_info = read_text_from_video(video_path, video_mapping[video_name])
        video_data['keywords'] += textual_info

        print("---> Audio in video being processed...")
        video.audio.write_audiofile(audio_temp_path, verbose=False)
        audio_info = transcribe_large_audio(audio_temp_path, video_mapping[video_name])
        video_data['keywords'] += audio_info

        video_data['keywords'] = list(set(video_data['keywords']))

        print("---> Saving thumbnail...")
        thumbnail = save_thumbnail(video, video_name)
        video_data["thumbnail"] = thumbnail

        print("Finishing recognition of video {}".format(video_name))

        video.close()
        shutil.rmtree('audio-chunks', ignore_errors=True)

        data.append(video_data)

    with open(data_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

def check_data():
    path = os.path.join(dir, data_filename)
    if not os.path.exists(path):
        process_videos()
        return True
    else:
        if os.stat(path).st_size == 0:
            process_videos()
            return True
        else:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if not data:
                    process_videos()
                    return True
                else:
                    return True