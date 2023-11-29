import os
from http import HTTPStatus
from flask import Blueprint, request, jsonify
from moviepy.editor import *

subtitle_api = Blueprint('subtitle', __name__)

# pip install translatesubs (working)
@subtitle_api.route('/add_blank_line_to_srt', methods=['POST'])
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

    response_object = {
        'status': 'success',
        'message': 'Successfully.'
    }

    return response_object, 200

@subtitle_api.route('/add_signature_to_video', methods=['POST'])
def add_signature_to_video():
    file_video = request.files["video"]
    video_path = os.path.join("uploads", file_video.filename)
    file_video.save(video_path)
    # Load the video
    video_clip = VideoFileClip(video_path)
    duration = video_clip.duration
    # Create a TextClip with the signature text
    signature_text = request.form['signature_text']
    text_clip = TextClip(signature_text, fontsize=50, color='white', font='Arial')

    def position(t):
        x = 10 * t  # Adjust the movement on the x-axis based on time
        y = 20 * t
        return (x,y)


    text_clip = TextClip(signature_text, fontsize=20, color='white', font='Arial').set_position(position).set_duration(420)

#     final = video_clip.fl(lambda gf, t: position(t))

    final = CompositeVideoClip([video_clip, text_clip])
    # Write the video with the signature text
    final.write_videofile(os.path.join("uploads",'video_with_signature_text.mp4'), codec='libx264', audio_codec='aac')

    response_object = {
        'status': 'success',
        'message': 'Successfully.'
    }

    return response_object, 200