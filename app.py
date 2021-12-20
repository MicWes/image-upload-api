import os
import requests
from flask import Flask, Response, render_template, request

# pylint: disable=C0103
app = Flask(__name__)

@app.route('/')
def hello():
    message = "Image Upload API is running!"

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

q = Queue() #instance queue

@app.route('/imgup', methods=['POST'])
def image_up():
    image = request.files['image']
    if image:
        q.enqueue(image)
        try:
            #request resize
            img = q.dequeue()
            
            size = request.args.get("size")
            if size:
                url_resize = "http://127.0.0.1:5000/resize?size=" + size
                response = requests.post(url_resize, files={'image' : img}, json={'size' : size})
            else:
                url_resize = "http://127.0.0.1:5000/resize"
                response = requests.post(url_resize, files={'image' : img})
            return Response(response.content, mimetype='image/jpg'), 200 #return image
        except:
            return 'Error: system error.', 500
    else:
        return 'Error: image not found.', 404

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
