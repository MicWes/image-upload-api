import os
import requests
from flask import Flask, render_template, request, jsonify
from PIL import Image

# pylint: disable=C0103
app = Flask(__name__)

@app.route('/')
def hello():
    message = "Image upload is running!"

    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)

class Queue: #FIFO
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

@app.route('/imgup', methods=['POST'])
def image_up():
    image = request.files['image']
    if image:
        q = Queue() #instance
        q.enqueue(image)
        try:
            #request resize
            img = q.dequeue()
            url_resize = "http://127.0.0.1:5000/resize"
            requests.post(url_resize, files={'image' : img})
            return 'image upload queue', 200
        except:
            return 'error', 500
    else:
        return 'error', 404

@app.route('/resize', methods=['POST'])
def resize():
    image = request.files['image']
    
    if image:
        #resizing
        img = Image.open(image)
        new_img = img.resize((384, 384))
        new_img.save('image_384.jpg')
        return 'ok', 200
    else:
        return 'error', 500

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
