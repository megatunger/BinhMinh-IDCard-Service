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
    birthday = request.args.get('birthday', ' ')
    school = request.args.get('school', ' ')
    phone = request.args.get('phone', ' ')
    id_encrypt = request.args.get('id_encrypt', ' ')
    return process(id, name, birthday, school, phone, id_encrypt)

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

def process(id, name, birthday, school, phone, id_encrypt):
    # Set params
    string_limit = 21
    id = id[:string_limit]
    name = name[:string_limit]
    birthday = birthday[:string_limit]
    school = school[:string_limit]
    phone = phone[:string_limit]
    id_encrypt = id_encrypt
    # opening image
    img = Image.open("plain.png")
    draw = ImageDraw.Draw(img)

    # opening font files
    font_regular = ImageFont.truetype("fonts/Montserrat-Regular.otf", 64)
    font_bold = ImageFont.truetype("fonts/Montserrat-SemiBold.otf", 64)

    # Writing text at specific positions and specific color.
    left_margin = 475
    start_text = 412.5
    line_spacing = 132

    draw.text((left_margin, start_text), id, (74, 75, 76), font=font_bold)
    draw.text((left_margin, start_text + line_spacing), name, (74, 75, 76), font=font_regular)
    draw.text((left_margin, start_text + line_spacing*2), birthday, (74, 75, 76), font=font_regular)
    draw.text((left_margin, start_text + line_spacing*3), school, (74, 75, 76), font=font_regular)
    draw.text((left_margin, start_text + line_spacing*4), phone, (74, 75, 76), font=font_regular)

    # Create qr image
    qr = pyqrcode.create('{"login_token":"'+id_encrypt+'","otp": "offline_card"}')

    filename_qr_png = 'output/qr/' + id + '.png'
    os.makedirs(os.path.dirname(filename_qr_png), exist_ok=True)

    qr.png(filename_qr_png, scale=8)

    # QR image is superimposed on the ID-card image with itself as a filter
    qr_img = Image.open(filename_qr_png)
    img.paste(qr_img, (1334, 383))

    #Save to disk

    filename_png = 'output/png/' + id + '.png'
    os.makedirs(os.path.dirname(filename_png), exist_ok=True)

    img.save(filename_png)

    # To convert to pdf the image is temporarily stored as jpeg
    rgb_img = img.convert('RGB')
    rgb_img.save("temp.jpg")
    temp = Image.open("temp.jpg")

    # The jpeg file is converted to pdf.
    pdf_bytes = img2pdf.convert("temp.jpg")

    filename_pdf = 'output/pdf/' + id + '.pdf'
    os.makedirs(os.path.dirname(filename_pdf), exist_ok=True)

    file = open(filename_pdf, "wb")
    file.write(pdf_bytes)
    os.remove("temp.jpg")

    return {'card_image': filename_png, 'qr_image': filename_qr_png, 'pdf': filename_pdf}

if __name__ == '__main__':
    app.run()
