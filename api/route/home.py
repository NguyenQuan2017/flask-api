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
from pydub.playback import play


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
    input_srt_file = '/home/pc14/QUAN/flask-api/test_vi.srt'
    output_audio_file = 'audio.wav'
    video_file = '/home/pc14/QUAN/flask-api/test.mp4'
    output_video_file = '/home/quannv/QUAN/flask-api/test_map.mp4'
    # Phân tích tệp SRT
    with open(input_srt_file, 'r', encoding='utf-8') as srt_file:
        srt_lines = srt_file.readlines()

    # Chuẩn bị video và audio
    video_clip = mp.VideoFileClip(video_file)
    audio = mp.AudioFileClip(video_file)
    audio = video_clip.audio
    audio.write_audiofile("audio.mp3")
#     audio = audio.set_duration(video_clip.duration)
#     final_audio = mp.CompositeAudioClip([audio])
    audio_clips = []
#     video_clips = []
    count = 0
    # Tạo audio cho từng phụ đề và đồng bộ hóa với video
    for i in range(0, len(srt_lines), 4):
#         if count == 4:
#             break
        time_line = srt_lines[i + 1].strip()
        if is_valid_time_format(time_line):
            start_time, end_time = time_line.split(' --> ')
            text = srt_lines[i + 2].strip()
            tts = gTTS(text, lang='vi')
            tts.save(f"audio.mp3")
#             audio = AudioSegment.from_file("audio.mp3")
            audio_clip = mp.AudioFileClip(f"audio.mp3")
#             audio_clips.append(audio_clip)
#             mapped_audio = audio.speedup(playback_speed=1.5)
#             mapped_audio.export("output_mapped_audio.mp3", format="mp3")
#             audio_clip = mp.AudioFileClip(f"output_mapped_audio.mp3")
#             audio_clip = audio_clip.set_start(start_time)
            audio_clips.append(audio_clip)
#         count += 1

#             audio_clip = audio_clip.set_end(end_time)
#             audio_clip.write_audiofile(f"audio_{i}.mp3", fps=44100)
#             video_subclip = video_clip.subclip(start_time, end_time)
#             video_subclip.write_videofile("temp_video.mp4")
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
#             video_with_synthesized_audio = video_subclip.set_audio(audio_clip)
#             video_with_synthesized_audio.write_videofile(f"output_video_merge.mp4", codec="libx264")
#             video_clips.append(video_with_synthesized_audio)
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

#     final = mp.CompositeAudioClip(audio_clips)
#     final.write_audiofile("final_audio.mp3", fps=44100)

    # Kết hợp (merge) các audio trong danh sách
    merged_audio = mp.concatenate_audioclips(audio_clips)
#     final_audio = mp.CompositeAudioClip(audio_clips)
    # Lưu âm thanh kết hợp thành tệp mới
    merged_audio.write_audiofile("merged_audio.mp3", fps=44100)
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


@home_api.route('/create_voice_v2', methods=['POST'])
def create_voice_v2():
    file_srt = request.files["file_srt"]
    file_path_srt = os.path.join("uploads", file_srt.filename)
    file_srt.save(file_path_srt)
    file_video = request.files["file_video"]
    file_path_video = os.path.join("uploads", file_video.filename)
    file_video.save(file_path_video)
    video_clip = mp.VideoFileClip(file_path_video)
    # Thay thế các giá trị này bằng thông tin tài khoản và ứng dụng của bạn
    input_srt_file = file_path_srt
    output_audio_file = 'output_audio.mp3'
    video_file = file_path_video
    # Phân tích tệp SRT
    with open(input_srt_file, 'r', encoding='utf-8') as srt_file:
        srt_lines = srt_file.readlines()
    audio_clips = []
    count = 0
    # Tạo audio cho từng phụ đề và đồng bộ hóa với video
    for i in range(0, len(srt_lines), 4):
#         if count == 1:
#             break
        time_line = srt_lines[i + 1].strip()
        if is_valid_time_format(time_line):
            start_time, end_time = time_line.split(' --> ')
            text = srt_lines[i + 2].strip()
            url = 'https://api.fpt.ai/hmi/tts/v5'
            video_subclip = video_clip.subclip(start_time, end_time)
            video_subclip.write_videofile("temp_video.mp4")
            video_subclip = mp.VideoFileClip('temp_video.mp4')
            audio = video_subclip.audio
            temp_audio_file = "temp_audio.mp3"  # You can change the format if needed
            audio.write_audiofile(temp_audio_file, fps=44100)
            exported_audio = AudioSegment.from_file(temp_audio_file)

                # Get the duration of the audio in milliseconds
            audio_duration = len(exported_audio)

                # Convert milliseconds to seconds
#             print(f"The speed of the voice in the video is approximately: {audio_duration}")
            # Convert milliseconds to seconds
            audio_duration_seconds = audio_duration / 1000
            print (f"Speed ratio {audio_duration_seconds}")
            # Get the number of words spoken in the audio (you might need a more accurate method)
            # For simplicity, assuming an average speech rate of 150 words per minute
            word_count = audio_duration_seconds  # Adjust this value based on the actual speech rate

            # Calculate the speed (words per second)
            speed = audio_duration_seconds
            payload = text
            headers = {
                'api-key': 'g3LLsjoYh7NlSM5i5dAcuyHooN8mS5st',
                'speed': '',
                'voice': 'banmai'
            }

            response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                audio_url = response_data.get('async')

                # Tải tệp âm thanh đã tạo từ URL
                audio_response = requests.get(audio_url)

                if audio_response.status_code == 200:
                    with open(output_audio_file, 'wb') as audio_file:
                        audio_file.write(audio_response.content)
                        audio_clip = AudioSegment.from_file("output_audio.mp3")
#                         words = len(text.split())
#                         duration = len(audio_clip) / 1000
#
#                         current_speed = words / duration
#                         speed_ratio = speed / current_speed
#                         print (f"Speed ratio {speed} : {current_speed}: {speed_ratio}")
                        # Apply the speed change to the audio
                        adjusted_audio = audio_clip._spawn(audio_clip.raw_data, overrides={
                            "frame_rate": int(audio_clip.frame_rate * 1)
                        }).set_frame_rate(audio_clip.frame_rate)
#                         adjusted_audio.write_audiofile("adjusted_audio.mp3", fps=44100)
                        adjusted_audio.export("adjusted_audio.mp3", format="mp3")
                        audio_export = mp.AudioFileClip("adjusted_audio.mp3")
#                         audio_export.set_start(start_time)
                        audio_clips.append(audio_export)
#             count +=1
    # Kết hợp (merge) các audio trong danh sách
    merged_audio = mp.concatenate_audioclips(audio_clips)
#     # Lưu âm thanh kết hợp thành tệp mới
    merged_audio.write_audiofile("merged_audio.mp3", fps=44100)
    os.remove(file_path_srt)
    os.remove(file_path_video)
    os.remove(output_audio_file)
    return 'success'
@home_api.route('/add_audio_to_video', methods=['POST'])
def add_audio_to_video():
    video_file = request.files["video_file"]
    file_path_video = os.path.join("uploads", video_file.filename)
    video_file.save(file_path_video)
    audio_file = request.files["audio_file"]
    file_path_audio = os.path.join("uploads", audio_file.filename)
    audio_file.save(file_path_audio)

    video_clip = mp.VideoFileClip(file_path_video)
    audio_clip = mp.AudioFileClip(file_path_audio)
    if video_clip.duration > audio_clip.duration:
        video_clip = video_clip.subclip(0, audio_clip.duration)
    # Set the audio duration same as video duration
#     audio_clip = audio_clip.set_duration(video_clip.duration)

    # Set the audio to the video file
    video_with_audio = video_clip.set_audio(audio_clip)

    # Specify the output file path for the video with added audio
    output_path = 'video_with_audio.mp4'

    # Write the final video file
    video_with_audio.write_videofile(output_path, codec='libx264', audio_codec='aac')

    os.remove(file_path_video)
    os.remove(file_path_audio)

    return 'success'
@home_api.route('/get_voice_speed', methods=['POST'])
def get_voice_speed(video_path):
#     video_path = '/home/pc14/QUAN/flask-api/test.mp4'
    video = mp.VideoFileClip(video_path)
    audio = video.audio

    # Get the duration of the audio in seconds
    audio_duration = audio.duration

    # Count the number of words in the audio
    # This method might not be highly accurate but can give an approximate idea
    # You may need a more sophisticated speech recognition system for better accuracy
    words = audio.to_soundarray()
    print(f"The speed of the voice in the video is approximately: {words}")
    word_count = len(words)

    # Calculate speed (words per second)
    speed = word_count / audio_duration

    print(f"The speed of the voice in the video is approximately: {speed:.2f} words per second")
    return 'success'

