from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from
from api.model.welcome import WelcomeModel
from api.schema.welcome import WelcomeSchema
import os
from srtranslator import SrtFile
from srtranslator.translators.translatepy import TranslatePy
import requests
import moviepy.editor as mp
import re
from gtts import gTTS
from pydub import AudioSegment

home_api = Blueprint('api', __name__)


@home_api.route('/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Welcome to the Flask Starter Kit',
            'schema': WelcomeSchema
        }
    }
})

def welcome():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = WelcomeModel()
    return WelcomeSchema().dump(result), 200

@home_api.route('/translate_subtitle', methods=['POST'])
def translate_subtitle(file_path, sourceTranslate, destinationTranslate):
    # pip install translatesubs (working)
    translator = TranslatePy()
#     file_path = '/home/quannv/QUAN/flask-api/captions.srt'
    srt = SrtFile(file_path)
    srt.translate(translator, sourceTranslate, destinationTranslate)

    # Making the result subtitles prettier
    srt.wrap_lines()
    path_translate = f"{os.path.splitext(file_path)[0]}_{destinationTranslate}_translated.srt"
    srt.save(f"{path_translate}")
    return 'success'
    response_object = {
        'status': 'success',
        'message': 'Successfully.'
    }
    return response_object, 200

@home_api.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        upload_directory = '/home/quannv/QUAN/flask-api'  # Change this to your desired directory
        file.save(os.path.join(upload_directory, file.filename))
        saved_directory = os.path.join(upload_directory, file.filename)
        translate_subtitle(saved_directory, request.form['source'], request.form['destination'])
        response_object = {
            'status': 'success',
            'message': 'Successfully.'
        }
        return response_object, 200
@home_api.route('/create_voice', methods=['POST'])
def create_voice():
    # Thay thế các giá trị này bằng thông tin tài khoản và ứng dụng của bạn
    input_srt_file = '/home/quannv/QUAN/flask-api/test_vi_translated.srt'
    output_audio_file = 'audio.wav'
    video_file = '/home/quannv/QUAN/flask-api/test.mp4'
    output_video_file = '/home/quannv/QUAN/flask-api/test_map.mp4'
    # Phân tích tệp SRT
    with open(input_srt_file, 'r', encoding='utf-8') as srt_file:
        srt_lines = srt_file.readlines()

    # Chuẩn bị video và audio
    video_clip = mp.VideoFileClip(video_file)
    audio = mp.AudioFileClip(video_file)
    audio = audio.set_duration(video_clip.duration)
    final_audio = mp.CompositeAudioClip([audio])
    audio_clips = []
    # Tạo audio cho từng phụ đề và đồng bộ hóa với video
    for i in range(0, len(srt_lines), 4):
        time_line = srt_lines[i + 1].strip()
        if is_valid_time_format(time_line):
            start_time, end_time = time_line.split(' --> ')
            text_lines = []
            for line in srt_lines[2:]:
                cleaned_line = line.strip()
                if not cleaned_line:
                    break  # Nếu gặp dòng trắng, dừng vòng lặp
                text_lines.append(cleaned_line)
            text = " ".join(text_lines)
            tts = gTTS(text, lang='vi')
            tts.save(f"audio_{i}.mp3")
            audio_clip = mp.AudioFileClip(f"audio_{i}.mp3")
            audio_clip = audio_clip.set_start(start_time)
            audio_clip = audio_clip.set_end(end_time)
            audio_clips.append(audio_clip)
#             final_audio = mp.CompositeAudioClip([audio_clip])
#             url = 'https://api.fpt.ai/hmi/tts/v5'
#
#             payload = text
#             headers = {
#                 'api-key': 'LWl9TqVVuD4WqJBkIGAVP11IHb7c5EM3',
#                 'speed': '',
#                 'voice': 'banmai'
#             }
#
#             response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)
#
#             if response.status_code == 200:
#                 response_data = response.json()
#                 audio_url = response_data.get('async')
#
#                 # Tải tệp âm thanh đã tạo từ URL
#                 audio_response = requests.get(audio_url)
#
#                 if audio_response.status_code == 200:
#                     with open(output_audio_file, 'wb') as audio_file:
#                         audio_file.write(audio_response.content)
#                         audio_clip = mp.AudioFileClip(audio_file)
#                         audio_clip = audio_clip.set_start(start_time)
#                         audio_clip = audio_clip.set_end(end_time)
#                         final_audio = mp.CompositeAudioClip([final_audio, audio_clip])
    # Kết hợp (merge) các audio trong danh sách
    merged_audio = mp.CompositeAudioClip(audio_clips)

    # Lưu âm thanh kết hợp thành tệp mới
    merged_audio.write_audiofile("merged_audio.mp3", fps=44100)
    # Đồng bộ hóa audio và video
    video_clip = video_clip.set_audio(merged_audio)

    # Xuất video đồng bộ hóa âm thanh
    video_clip.write_videofile(output_video_file, codec="libx264", audio_codec="aac")

    return 'success'

def is_valid_time_format(time_str):
    # Định dạng thời gian "HH:MM:SS,sss --> HH:MM:SS,sss" (giờ, phút, giây, mili-giây)
    time_format = r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}'
    return bool(re.match(time_format, time_str))