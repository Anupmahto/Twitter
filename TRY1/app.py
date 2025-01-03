from flask import Flask, render_template, jsonify
from utils.scraper import TwitterScraper
from utils.db_handler import DatabaseHandler

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape_trends():
    try:
        # Initialize scraper and database handler
        scraper = TwitterScraper()
        db = DatabaseHandler()
        
        # Scrape trends
        trends_data = scraper.scrape()
        
        # Save to database
        db.save_trends(trends_data)
        
        # Close database connection
        db.close_connection()
        
        return jsonify({
            'status': 'success',
            'data': trends_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)