import os

from flask import Flask, render_template, request, jsonify

# pylint: disable=C0103
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
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
        #request
        return 'image', 200
    else:
        return 'error', 404

@app.route('/resize', methods=['POST'])
def resize():
    image = request.files['image']
    #resizing
    return

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
