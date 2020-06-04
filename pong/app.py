from flask import Flask, request
from db import db_links

app = Flask(__name__)

@app.route('/ping/', methods=['POST'])
def ping():
    if request.method == 'POST':
        ping_from = request.headers.get('Ping-From')
        ping_to = request.headers.get('Ping-To')
        if item := db_links.find_one({'link': ping_to}):
            item['count'] += 1
            db_links.update_one({'link': ping_to}, {'$set': item})
        else:
            item = {
                'link': ping_to,
                'count': 1
            }
            db_links.insert_one(item)

        return ping_to
        


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
