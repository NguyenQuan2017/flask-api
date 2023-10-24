from http import HTTPStatus
from flask import Blueprint, request, jsonify
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
import speech_recognition as sr
from datetime import datetime, timedelta
import cv2

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
    path__format_translate = f"{os.path.splitext(file_path)[0]}_{destinationTranslate}_format_translated.srt"
    srt.save(f"{path_translate}")
    format_srt_content_oneline(path_translate, path__format_translate)
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
    input_srt_file = '/home/quannv/QUAN/flask-api/test_vi_format_translated.srt'
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
    video_clips = []
    count = 0
    # Tạo audio cho từng phụ đề và đồng bộ hóa với video
    for i in range(0, len(srt_lines), 4):
        time_line = srt_lines[i + 1].strip()
        if is_valid_time_format(time_line):
            start_time, end_time = time_line.split(' --> ')
            text = srt_lines[i + 2].strip()
            tts = gTTS(text, lang='vi')
            tts.save(f"audio.mp3")
            audio_clip = mp.AudioFileClip(f"audio.mp3")
#             audio_clip = audio_clip.set_start(start_time)
#             audio_clip = audio_clip.set_end(end_time)
#             audio_clip.write_audiofile(f"audio_{i}.mp3", fps=44100)
            video_subclip = video_clip.subclip(start_time, end_time)
            video_subclip.write_videofile("temp_video.mp4")
#             text_clip = mp.TextClip(text, fontsize=30, color='white')
            # Mix văn bản với video
#             result_video = mp.CompositeVideoClip([video_subclip, text_clip.set_position('bottom').set_duration(video_subclip.duration)])
            # Lưu video kết quả
#             result_video.write_videofile(f"output_video.mp4")
#             recognizer = sr.Recognizer()
#             audio = sr.AudioFile("temp_video.mp4")
#             input_audio = AudioSegment.from_file("input_audio.wav", format="wav")
#             with audio as source:
#                 audio_text = recognizer.recognize_google(source)

            # Tạo âm thanh tổng hợp từ văn bản
#             tts = gTTS(text, lang='vi')
#             tts.save("segmented_audio.mp3")
#             audio = AudioSegment.from_file("synthesized_audio.mp3", format="mp3")
#             time_format = "%H:%M:%S,%f"
#             start_time_obj = datetime.strptime(start_time, time_format)
#             end_time_obj = datetime.strptime(end_time, time_format)

            # Chuyển đổi đối tượng datetime thành mili giây
#             start_time_ms = (start_time_obj - datetime.min).total_seconds() * 1000
#             end_time_ms = (end_time_obj - datetime.min).total_seconds() * 1000
#             segmented_audio = audio[start_time_ms:end_time_ms]
#             segmented_audio.export("segmented_audio.mp3", format="mp3")
            # Hợp nhất âm thanh tổng hợp với video
#             synthesized_audio = mp.AudioFileClip("segmented_audio.mp3")
            video_with_synthesized_audio = video_subclip.set_audio(audio_clip)
#             video_with_synthesized_audio.write_videofile(f"output_video_merge.mp4", codec="libx264")
            video_clips.append(video_with_synthesized_audio)
#             video_with_synthesized_audio.write_videofile(f"output_video_{i}.mp4", codec="libx264")
#             video_with_audio = video_subclip.set_audio(audio_clip)
#             video_with_audio.write_videofile(f"output_video_{i}.mp4", codec="libx264")
#             final_audio = mp.CompositeAudioClip([final_audio, audio_clip])
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
    final = mp.concatenate_videoclips(video_clips)
    final.write_videofile("merged.mp4")

    # Kết hợp (merge) các audio trong danh sách
#     merged_audio = mp.concatenate_audioclips(audio_clips)
#     final_audio = mp.CompositeAudioClip(audio_clips)
    # Lưu âm thanh kết hợp thành tệp mới
#     merged_audio.write_audiofile("merged_audio.mp3", fps=44100)
    # Đồng bộ hóa audio và video
#     video_clip = video_clip.set_audio(final_audio)

    # Xuất video đồng bộ hóa âm thanh
#     video_clip.write_videofile(output_video_file, codec="libx264", audio_codec="aac")

    return 'success'

def is_valid_time_format(time_str):
    # Định dạng thời gian "HH:MM:SS,sss --> HH:MM:SS,sss" (giờ, phút, giây, mili-giây)
    time_format = r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}'
    return bool(re.match(time_format, time_str))

def format_srt_content_oneline(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as input_srt, open(output_file, 'w', encoding='utf-8') as output_srt:
        lines = input_srt.readlines()
        current_time_info = ""
        current_subtitle_order = 1
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if line == "":
                current_subtitle_order = formatted_lines[0]
                current_time_info = formatted_lines[1]
                formatted_lines.remove(current_subtitle_order)
                formatted_lines.remove(current_time_info)
                # Dòng trống thường kết thúc một phụ đề, ghép nội dung lại với nhau
                formatted_line = current_subtitle_order + "\n" + current_time_info + "\n" + " ".join(formatted_lines) + "\n\n"
                formatted_lines = []  # Đặt lại danh sách nội dung
                output_srt.write(formatted_line)
            else:
                formatted_lines.append(line)
@home_api.route("/add_blank_line_to_srt", methods=["POST"])
def add_blank_line_to_srt():
    if request.method == "POST":
            # Kiểm tra xem đã tải lên tệp tin SRT hay chưa
            if "file" not in request.files:
                return "Chưa tải lên tệp nào."

            file = request.files["file"]

            # Kiểm tra xem tệp tin có tồn tại và có phải là SRT không
            if file and file.filename.endswith(".srt"):
                # Lưu tệp tin tải lên vào thư mục tạm
                file_path = os.path.join("uploads", file.filename)
                file.save(file_path)

                with open(file_path, "r", encoding="utf-8") as file:
                   srt_content = file.readlines()

                # Thêm dòng trắng vào vị trí +4 (sau mỗi 4 dòng)
                modified_srt = []
                for i, line in enumerate(srt_content):
                    modified_srt.append(line)
                    if (i + 1) % 3 == 0:
                        modified_srt.append("\n")

                # Ghi lại nội dung đã được chỉnh sửa vào tệp tin
                with open(file_path, "w", encoding="utf-8") as file:
                    file.writelines(modified_srt)

                return "Đã thêm dòng trắng vào tệp SRT."
