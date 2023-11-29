import os
import requests
from http import HTTPStatus
from flask import Blueprint, request, jsonify
from srtranslator import SrtFile
from srtranslator.translators.translatepy import TranslatePy
import moviepy.editor as mp
from datetime import datetime, timedelta
from pydub import AudioSegment
import re
import time

create_voice_api = Blueprint('create_voice', __name__)

@create_voice_api.route('/create_voice', methods=['POST'])

def create_voice():
    file_srt = request.files["file_srt"]
    file_video = request.files["file_video"]
    #
    file_path_srt = os.path.join("uploads", file_srt.filename)
    file_srt.save(file_path_srt)
    file_path_video = os.path.join("uploads", file_video.filename)
    file_video.save(file_path_video)
    video_clip = mp.VideoFileClip(file_path_video)

    output_audio_file = 'temp/output_audio.mp3'
    video_file = file_path_video
    # Phân tích tệp SRT
    with open(file_path_srt, 'r', encoding='utf-8') as srt_file:
        srt_lines = srt_file.readlines()
    audio_clips = []
    count = 0
    # Tạo audio cho từng phụ đề và đồng bộ hóa với video
    for i in range(0, len(srt_lines), 4):
        time_line = srt_lines[i + 1].strip()
        if is_valid_time_format(time_line):
            start_time, end_time = time_line.split(' --> ')
            text = srt_lines[i + 2].strip()
            url = 'https://api.fpt.ai/hmi/tts/v5'
            payload = text
            headers = {
                'api-key': '94xB69ZMrUOTEn3d5e7UbbAHoedTfGnO',
                'speed': '',
                'voice': 'banmai'
            }

            response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                print(text)
                audio_url = response_data.get('async')

                # Tải tệp âm thanh đã tạo từ URL
                audio_response = requests.get(audio_url)
                if audio_response.status_code == 200:
                    with open(output_audio_file, 'wb') as audio_file:
                        audio_file.write(audio_response.content)
                        audio_clip = AudioSegment.from_file("output_audio.mp3")
                        adjusted_audio = audio_clip._spawn(audio_clip.raw_data, overrides={
                            "frame_rate": int(audio_clip.frame_rate * 1)
                        }).set_frame_rate(audio_clip.frame_rate)
                        adjusted_audio.export("adjusted_audio.mp3", format="mp3")
                        audio_export = mp.AudioFileClip("adjusted_audio.mp3")
                        audio_export = mp.AudioFileClip("adjusted_audio.mp3")
                        audio_clips.append(audio_export)
            else:
                print(response.json())
            time.sleep(1)
    # Kết hợp (merge) các audio trong danh sách
    merged_audio = mp.concatenate_audioclips(audio_clips)
    # Lưu âm thanh kết hợp thành tệp mới
    merged_audio.write_audiofile("merged_audio.mp3", fps=44100)
    merged_audio = mp.AudioFileClip("merged_audio.mp3")
    audio_duration = merged_audio.duration
    new_video = video_clip.set_duration(audio_duration)
    video_with_new_audio = new_video.set_audio(merged_audio)
    video_with_new_audio.write_videofile("final_video.mp4", codec='libx264', audio_codec='aac')
    os.remove(file_path_srt)
    os.remove(file_path_video)
    os.remove(output_audio_file)

    response_object = {
        'status': 'success',
        'message': 'Successfully.'
    }

    return response_object, 200

def is_valid_time_format(time_str):
    # Định dạng thời gian "HH:MM:SS,sss --> HH:MM:SS,sss" (giờ, phút, giây, mili-giây)
    time_format = r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}'
    return bool(re.match(time_format, time_str))
