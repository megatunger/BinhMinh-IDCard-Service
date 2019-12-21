from flask import Flask, request
import sys
import os
import img2pdf
import pyqrcode
from PIL import Image, ImageOps, ImageFont, ImageDraw

app = Flask(__name__)


@app.route('/')
def get():
    return 'POST request available only.'

@app.route('/', methods = ['POST'])
def main():
    id = request.args.get('id', ' ')
    name = request.args.get('name', ' ')
    birthday = request.args.get('birthday', ' ')
    school = request.args.get('school', ' ')
    phone = request.args.get('phone', ' ')
    return process(id, name, birthday, school, phone)

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

if __name__ == '__main__':
    app.run()


def process(id, name, birthday, school, phone):
    # Set params
    string_limit = 21
    id = id[:string_limit]
    name = name[:string_limit]
    birthday = birthday[:string_limit]
    school = school[:string_limit]
    phone = phone[:string_limit]

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
    qr = pyqrcode.create(id)
    filename = 'output/qr/' + id + '.png'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    qr.png(filename, scale=16)

    # QR image is superimposed on the ID-card image with itself as a filter
    qr_img = Image.open(filename)
    img.paste(qr_img, (1334, 383))

    #Save to disk
    img.save(filename)

    # To convert to pdf the image is temporarily stored as jpeg
    rgb_img = img.convert('RGB')
    rgb_img.save("temp.jpg")
    temp = Image.open("temp.jpg")

    # The jpeg file is converted to pdf.
    pdf_bytes = img2pdf.convert("temp.jpg")
    file = open("output/pdf/" + id + ".pdf", "wb")
    file.write(pdf_bytes)
    os.remove("temp.jpg")

    return {'card_image': 'output/png/' + id + '.png', 'qr_image':'output/qr/' + id + '.png', 'pdf': 'output/pdf/' + id + '.pdf'}