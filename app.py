from flask import Flask, jsonify, request
from flask_cors import CORS
from analytics.pagerank import TwitterGraph
import mysql.connector
from dotenv import load_dotenv
import os
from main import start_crawl  # Import crawling function
from datetime import datetime

app = Flask(__name__)
CORS(app)
load_dotenv()

@app.route('/api/crawl', methods=['POST'])
def crawl_data():
    try:
        success = start_crawl()  # Execute crawling
        return jsonify({
            'status': 'success' if success else 'error',
            'message': 'Crawling completed successfully' if success else 'Crawling failed'
        }), 200 if success else 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Global graph instance to maintain weights
graph = TwitterGraph()

@app.route('/api/weights', methods=['POST'])
def update_weights():
    try:
        new_weights = request.json
        if not isinstance(new_weights, dict):
            return jsonify({
                'status': 'error',
                'message': 'Invalid weights format'
            }), 400
            
        # Validate weights
        for key, value in new_weights.items():
            if not isinstance(value, (int, float)) or value < 0:
                return jsonify({
                    'status': 'error',
                    'message': f'Invalid weight value for {key}'
                }), 400

        # Update weights
        graph.set_weights(new_weights)
        
        return jsonify({
            'status': 'success',
            'message': 'Weights updated successfully',
            'weights': graph.weights
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error', 
            'message': str(e)
        }), 500

@app.route('/api/top-kols', methods=['GET'])
def get_top_kols():
    try:
        # Try to load cached rankings
        cache_data = graph.load_cached_rankings()
        
        if cache_data is None:
            # No valid cache, return message to compute first
            return jsonify({
                'status': 'error',
                'message': 'No PageRank data available. Please compute PageRank first.',
                'cached': False
            }), 404
        
        # Cache exists, proceed with data fetching
        rankings = cache_data['rankings']
        timestamp = cache_data['timestamp']
        
        # Get top 10
        top_10_kols = rankings[:10]
        
        # Database connection and user details fetching
        conn = mysql.connector.connect(**graph.db_config)
        cursor = conn.cursor(dictionary=True)
        
        top_kol_ids = [kol_id for kol_id, _ in top_10_kols]
        placeholders = ','.join(['%s'] * len(top_kol_ids))
        
        cursor.execute(f"""
            SELECT 
                user_id,
                username,
                role,
                joined_at,
                following,
                follower as followers,
                posts_cnt,
                saved_at,
                updated_at
            FROM users 
            WHERE user_id IN ({placeholders})
        """, top_kol_ids)
        
        users_data = cursor.fetchall()
        scores_dict = dict(top_10_kols)
        
        for user in users_data:
            user['pagerank_score'] = float(scores_dict[user['user_id']])
            user['joined_at'] = user['joined_at'].isoformat()
            user['saved_at'] = user['saved_at'].isoformat()
            user['updated_at'] = user['updated_at'].isoformat()
            
        users_data.sort(key=lambda x: x['pagerank_score'], reverse=True)
        
        cursor.close()
        conn.close()

        return jsonify({
            'status': 'success',
            'cached': True,
            'computed_at': timestamp,
            'data': users_data
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    
@app.route('/api/compute-pagerank', methods=['POST'])
def compute_pagerank():
    try:
        graph.load_twitter_data()
        rankings = graph.get_kol_rankings()
        graph.save_rankings(rankings)
        
        return jsonify({
            'status': 'success',
            'message': 'PageRank computed and cached successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)