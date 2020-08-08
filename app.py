from flask import Flask, request, send_file, redirect, url_for, send_from_directory
import sys
import os
import img2pdf
import pyqrcode
from PIL import Image, ImageOps, ImageFont, ImageDraw

BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = 'output'

app = Flask(__name__)
@app.route('/')
def get():
    return 'POST request available only.'

@app.route('/output/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(BASE_DIR, UPLOAD_FOLDER)
    return send_from_directory(directory=uploads, filename=filename)


@app.route('/', methods = ['POST'])
def main():
    id = request.args.get('id', ' ')
    name = request.args.get('name', ' ')
    school = request.args.get('school', ' ')
    id_encrypt = request.args.get('id_encrypt', ' ')
    return process(id, name, school, id_encrypt)

@app.route('/', methods = ['DELETE'])
def clearCache():
    id = request.args.get('id', ' ')
    try:
        os.remove("output/png/" + id + ".png")
        os.remove("output/qr/" + id + ".png")
        os.remove("output/pdf/" + id + ".pdf")
        return "success"
    except:
        return "file not found."

def process(id, name, school, id_encrypt):
    # Set params
    string_limit = 21
    id = id[:string_limit]
    name = name[:string_limit]
    school = school[:string_limit]
    id_encrypt = id_encrypt
    # opening image
    img_front = Image.open("Template/Front.png")
    img_back = Image.open("Template/Back.png")
    draw = ImageDraw.Draw(img_front)

    # opening font files
    font_regular = ImageFont.truetype("fonts/Montserrat-Regular.otf", 56)
    font_bold = ImageFont.truetype("fonts/Montserrat-SemiBold.otf", 56)

    # Writing text at specific positions and specific color.

    draw.text((193, 403), id, (22, 28, 42), font=font_bold)
    draw.text((193, 711), name, (22, 28, 42), font=font_bold)
    draw.text((193, 1010), school, (22, 28, 42), font=font_bold)

    # Create qr image
    qr = pyqrcode.create('{"login_token":"'+id_encrypt+'","otp": "offline_card"}')

    filename_qr_png = 'output/qr/' + id + '.png'
    os.makedirs(os.path.dirname(filename_qr_png), exist_ok=True)

    qr.png(filename_qr_png, scale=12)

    # QR image is superimposed on the ID-card image with itself as a filter
    qr_img = Image.open(filename_qr_png)
    img_front.paste(qr_img, (1215, 345))

    #Save to disk

    filename_front_png = 'output/png/' + id + '_front.png'
    filename_back_png = 'output/png/' + id + '_back.png'
    os.makedirs(os.path.dirname(filename_front_png), exist_ok=True)
    os.makedirs(os.path.dirname(filename_back_png), exist_ok=True)

    img_front.save(filename_front_png)
    img_front.save(filename_back_png)

    # To convert to pdf the image is temporarily stored as jpeg
    rgb_img_front = img_front.convert('RGB')
    rgb_img_back = img_back.convert('RGB')

    rgb_img_front.save("temp_front.jpg")
    rgb_img_back.save("temp_back.jpg")

    temp_front = Image.open("temp_front.jpg")
    temp_back = Image.open("temp_back.jpg")

    # The jpeg file is converted to pdf.
    pdf_bytes = img2pdf.convert(["temp_front.jpg", "temp_back.jpg"])

    filename_pdf = 'output/pdf/' + id + '.pdf'
    os.makedirs(os.path.dirname(filename_pdf), exist_ok=True)

    file = open(filename_pdf, "wb")
    file.write(pdf_bytes)
    os.remove("temp_front.jpg")
    os.remove("temp_back.jpg")

    return {'card_image': {'front': filename_front_png, 'back': filename_back_png}, 'qr_image': filename_qr_png, 'pdf': filename_pdf}

if __name__ == '__main__':
    app.run()
