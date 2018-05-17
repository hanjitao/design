from flask import jsonify, request, url_for, make_response
from . import api
from .. import db
from ..models import Poems, Loved_Poetry, New_Poetry
import socket
import time
import os

UPLOAD_FOLDER = "/root/work/design/app/images"


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'r') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream

@api.route('/upload_image', methods=['POST'])
def upload_image():
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    f = request.files['data']
    pid = request.form['pid']
    #poetry = request.form['poetry']
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    f.save(os.path.join(UPLOAD_FOLDER, f.filename))
    print(f.filename)
    try:
        poetry = New_Poetry.query.filter_by(id=pid).first()
        poetry.image_name = f.filename
        poetry.public = 1
        #poetry.save = 1
        poetry.public_time = int(time.time())

        db.session.commit()
        return jsonify({
            'message': 'success',
            'subjects': poetry.to_dict(),
        })
    except Exception as e:
        return jsonify({
            'message' : 'db error'
        })

    return jsonify({
        'message': 'success',
    })

@api.route('/get_image/<name>')
def get_image(name):
    print(name)
    name = 'tmp_0fe64c31220ab3e2f1f47745cce6f5678ea4cbe35d673500.jpg' if name == 'null' else name
    image_data = open(os.path.join(UPLOAD_FOLDER, name), "rb").read()

    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@api.route('/get_image_by_pid')
def get_image_by_pid():
    pid = request._args.get('pid', 0)
    poetry = New_Poetry.query.filter_by(id=pid).first()
    filename = poetry.image_name
    image_data = open(os.path.join(UPLOAD_FOLDER, filename), "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == '__main__':
    filename = "wx7940e4ebbf37a46d.o6zAJswR24QC9Xl3HqNre0bFt8XI.WcSn7ZCjhVVw3cb041fc154c35dd70718478cd4e5931.jpg"
    print(len(filename))
