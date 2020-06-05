import os
import pymongo
from flask import Flask, request, render_template

from db import db_link

app = Flask(__name__)
allow_ping_from_keyword = os.environ.get('ALLOW_PING_FROM_KEYWORD', default='')
allow_ping_from_keyword_list = allow_ping_from_keyword.split(',')
disallow_ping_to_keyword = os.environ.get('DISALLOW_PING_TO_KEYWORD', default='')
disallow_ping_to_keyword_list = disallow_ping_to_keyword.split(',')

@app.route('/ping/', methods=['POST'])
def ping():
    def match(s, keyword_list):
        if (not s) or (not keyword_list):
            return False
        for k in keyword_list:
            if k in s:
                return True
        return False

    ping_from = request.headers.get('Ping-From')
    # 有的时候 Ping-From 为空，则取 Origin
    if not ping_from:
        ping_from = request.headers.get('Origin')

    # 阻止其它网站盗用本服务
    if allow_ping_from_keyword and (not match(ping_from, allow_ping_from_keyword_list)):
        return "Unknown Origin: {}".format(ping_from)

    ping_to = request.headers.get('Ping-To')
    # 目的网址关键字黑名单, 防止小广告
    if disallow_ping_to_keyword and (match(ping_to, disallow_ping_to_keyword_list)):
        return "Blacklisted Destination: {}".format(ping_to)
    # 数据记录
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
