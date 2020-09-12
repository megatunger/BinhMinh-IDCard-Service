from flask import Flask, request, send_file, redirect, url_for, send_from_directory, send_file
import os
from PIL import Image, ImageOps, ImageFont, ImageDraw

BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = 'output'

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main():
    id = request.args.get('id', ' ')
    name = request.args.get('name', ' ')
    school = request.args.get('school', ' ')
    return send_file(process(id, name, school), as_attachment=True)

@app.route('/', methods = ['DELETE'])
def clearCache():
    id = request.args.get('id', ' ')
    try:
        os.remove("output/" + id + ".png")
        return "success"
    except:
        return "file not found."

def process(id, name, school):
    # Set params
    string_limit = 21
    id = id[:string_limit]
    name = name[:string_limit]
    school = school[:string_limit]
    # opening image
    img_front = Image.open("Template/Front.png")
    draw = ImageDraw.Draw(img_front)

    # opening font files
    font_bold = ImageFont.truetype("fonts/Rene Bieder - Gentona Bold.otf", 56)

    # Writing text at specific positions and specific color.

    draw.text((193, 403), id, (22, 28, 42), font=font_bold)
    draw.text((193, 711), name, (22, 28, 42), font=font_bold)
    draw.text((193, 1010), school, (22, 28, 42), font=font_bold)

    # Save to disk

    filename_front_png = 'output/' + id + '.png'
    os.makedirs(os.path.dirname(filename_front_png), exist_ok=True)

    img_front.save(filename_front_png)
    return filename_front_png

if __name__ == '__main__':
    app.run()
