from flask import Flask, jsonify, render_template
from scrapper import scrape_twitter
from proxy_manager import ProxyManager
from db_manager import DBManager
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

app = Flask(__name__)

proxy_manager = ProxyManager(os.getenv('PROXYMESH_URL'))
db_manager = DBManager('twitter_trends.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    proxy = proxy_manager.get_proxy()
    result = scrape_twitter(proxy)
    if result:
        db_manager.insert_trend(result)
        return jsonify({"message": "Scraping completed and data stored."})
    else:
        return jsonify({"message": "Scraping failed. Please check the logs for more information."}), 500

@app.route('/trends', methods=['GET'])
def get_trends():
    trends = db_manager.get_all_trends()
    return jsonify(trends)

if __name__ == '__main__':
    app.run(debug=True)

