import math
import pandas as pd
import numpy as np
import mysql.connector
from dotenv import load_dotenv
import os

class TwitterGraph:
    def __init__(self, damping_factor=0.85, convergence=1e-6, max_iterations=100):
        self.damping_factor = damping_factor
        self.convergence = convergence 
        self.max_iterations = max_iterations
        self.nodes = {}  # user_id -> node_index mapping
        self.edges = []  # List of (source, target, weight) tuples

        load_dotenv()
        self.db_config = {
            'host': os.getenv('HOST'),
            'user': os.getenv('USER'),
            'password': os.getenv('PASSWORD'),
            'database': os.getenv('DATABASE')
        }
        
    def add_edge(self, from_user, to_user, relationship_type):
        # Add nodes if not exist
        if from_user not in self.nodes:
            self.nodes[from_user] = len(self.nodes)
        if to_user not in self.nodes:
            self.nodes[to_user] = len(self.nodes)
            
        # Weight based on relationship
        weight = {
            'follow': 1.0,
            'retweet': 2.0, 
            'comment': 1.5
        }.get(relationship_type, 1.0)
        
        self.edges.append((
            self.nodes[from_user], 
            self.nodes[to_user],
            weight
        ))

    def compute_pagerank(self):
        n = len(self.nodes)
        pr = np.ones(n) / n
        
        # Create adjacency matrix with weights
        adj_matrix = np.zeros((n, n))
        for src, dst, weight in self.edges:
            adj_matrix[dst][src] = weight
            
        # Normalize weights by column
        out_weights = np.sum(adj_matrix, axis=0)
        adj_matrix = np.divide(adj_matrix, out_weights, 
                             where=out_weights!=0)
        
        diff = float('inf')
        iterations = 0
        
        while diff > self.convergence and iterations < self.max_iterations:
            new_pr = np.zeros(n)
            
            # Handle dangling nodes
            dangling_nodes = np.where(out_weights == 0)[0]
            dangling_sum = sum(pr[i] for i in dangling_nodes)
            
            for i in range(n):
                # Get weighted sum from incoming edges
                incoming_pr = sum(pr[j] * adj_matrix[i][j] 
                                for j in range(n))
                
                new_pr[i] = ((1 - self.damping_factor) / n + 
                            self.damping_factor * (incoming_pr + 
                            dangling_sum / n))
            
            diff = np.sum(np.abs(new_pr - pr))
            pr = new_pr
            iterations += 1
            
        return pr

    def load_twitter_data(self):
        # Database connection
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()

        # Get relationships
        cursor.execute("""
            SELECT DISTINCT f.user_id, f.follower_user_id, 'follow' as type 
            FROM followers f
            UNION
            SELECT DISTINCT r.user_id, upt.user_id, 'retweet'
            FROM reposts r
            JOIN user_post_tweet upt ON r.tweet_id = upt.tweet_id
            UNION  
            SELECT DISTINCT uct.user_id, upt.user_id, 'comment'
            FROM user_comment_tweet uct
            JOIN user_post_tweet upt ON uct.tweet_id = upt.tweet_id
        """)
        
        for source, target, rel_type in cursor:
            self.add_edge(source, target, rel_type)
            
        cursor.close()
        conn.close()

    def get_rankings(self):
        scores = self.compute_pagerank()
        
        # Reverse mapping of indices to user_ids
        rev_nodes = {v: k for k,v in self.nodes.items()}
        
        # Create rankings list
        rankings = [(rev_nodes[i], score) 
                   for i, score in enumerate(scores)]
        
        return sorted(rankings, key=lambda x: x[1], reverse=True)

# Usage
graph = TwitterGraph()
graph.load_twitter_data()
rankings = graph.get_rankings()

print("\nRanking KOLs:")
for user_id, score in rankings:
    print(f"{user_id}: {score:.6f}")