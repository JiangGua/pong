import os
import pymongo
from flask import Flask, request, render_template

from db import db_link

app = Flask(__name__)
allow_ping_from_keyword = os.environ.get('ALLOW_PING_FROM_KEYWORD', default=None)

@app.route('/ping/', methods=['POST'])
def ping():
    if request.method == 'POST':
        ping_from = request.headers.get('Ping-From')

        # 阻止其它网站盗用本服务
        if allow_ping_from_keyword and (ping_from.find(allow_ping_from_keyword) == -1):
            return "Unknown Origin: {}".format(ping_from)

        ping_to = request.headers.get('Ping-To')
        if item := db_link.find_one({'link': ping_to, 'origin': ping_from}):
            item['count'] += 1
            db_link.update_one({'link': ping_to, 'origin': ping_from}, {'$set': item})
        else:
            item = {
                'link': ping_to,
                'count': 1,
                'origin': ping_from
            }
            db_link.insert_one(item)
        return ping_to
    else:
        return "Use POST method instead"
        
@app.route('/stats/')
def stats():
    links = list(db_link.find({}, {'_id': False}, sort=[("count", pymongo.DESCENDING)]))
    config = {
        'title': os.environ.get('SITE_TITLE', default='Stats - Pong'),
        'h1': os.environ.get('SITE_H1', default=None) or os.environ.get('SITE_TITLE', default='Stats - Pong')
    }
    return render_template('stats.html', config=config, links=links)

@app.route('/api/stats/')
def api_stats():
    links = list(db_link.find({}, {'_id': False}, sort=[("count", pymongo.DESCENDING)]))
    return {
        'links': links
    }

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
