import os
import pymongo
from flask import Flask, request, render_template

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
    else:
        return "Use POST method instead"
        
@app.route('/stats/')
def stats():
    links = list(db_links.find({}, sort=[("count", {'_id': False}, pymongo.DESCENDING)]))
    config = {
        'title': os.environ.get('SITE_TITLE', default='Stats - Pong'),
        'h1': os.environ.get('SITE_TITLE', default=None) or os.environ.get('SITE_TITLE', default='Stats - Pong')
    }
    return render_template('stats.html', config=config, links=links)

@app.route('/api/stats/')
def api_stats():
    links = list(db_links.find({}, {'_id': False}, sort=[("count", pymongo.DESCENDING)]))
    return {
        'links': links
    }

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
