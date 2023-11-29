import os
from http import HTTPStatus
from flask import Blueprint, request, jsonify
from srtranslator import SrtFile
from srtranslator.translators.translatepy import TranslatePy

translate_subtitle_api = Blueprint('translate_subtitle', __name__)

# pip install translatesubs (working)
@translate_subtitle_api.route('/translate_subtitle', methods=['POST'])
def translate_subtitle():
    if 'file' not in request.files:
            return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    source_translate = request.form['source']
    destination_translate = request.form['destination']

    if file:
        upload_directory = 'uploads'  # Change this to your desired directory
        file.save(os.path.join(upload_directory, file.filename))
        file_path = os.path.join(upload_directory, file.filename)
        translator = TranslatePy()
        srt = SrtFile(file_path)
        srt.translate(translator, source_translate, destination_translate)

#         # Making the result subtitles prettier
        srt.wrap_lines()
        path_translate = f"{os.path.splitext(file_path)[0]}_{destination_translate}.srt"
        path__format_translate = f"{os.path.splitext(file_path)[0]}_{destination_translate}_format.srt"
        srt.save(f"{path_translate}")
        format_srt_content_oneline(path_translate, path__format_translate)

        response_object = {
            'status': 'success',
            'message': 'Successfully.'
        }

        return response_object, 200

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