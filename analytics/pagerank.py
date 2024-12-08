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
        self.nodes = {}  # {id: {'index': idx, 'type': 'user|tweet'}}
        self.edges = []  # (source_idx, target_idx, weight, type)

        self.weights = {
            'follow': 1.0,
            'post': 2.0,
            'retweet': 1.5,
            'comment': 1.2,
            'mention': 0.8
        }
        
        load_dotenv()
        self.db_config = {
            'host': os.getenv('HOST'),
            'user': os.getenv('USER'),
            'password': os.getenv('PASSWORD'), 
            'database': os.getenv('DATABASE')
        }

    def set_weights(self, new_weights):
        # Update weights while keeping defaults for missing values
        self.weights.update(new_weights)

    def add_node(self, node_id, node_type):
        if node_id not in self.nodes:
            self.nodes[node_id] = {
                'index': len(self.nodes),
                'type': node_type
            }
        return self.nodes[node_id]['index']

    def add_edge(self, from_id, to_id, edge_type, from_type='user', to_type='user'):
        from_idx = self.add_node(from_id, from_type)
        to_idx = self.add_node(to_id, to_type)

        weight = self.weights.get(edge_type, 1.0)
        
        # Add bidirectional edges for certain relationships
        self.edges.append((from_idx, to_idx, weight, edge_type))
        if edge_type in ['retweet', 'comment']:
            self.edges.append((to_idx, from_idx, weight * 0.5, f'reverse_{edge_type}'))

    def load_twitter_data(self):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()

        # Get KOLs and their network
        cursor.execute("""
            WITH kols AS (
                SELECT user_id 
                FROM users 
                WHERE role = 'KOL'
            )
            -- KOL followers
            SELECT 'follow', f.follower_user_id, f.user_id, NULL as tweet_id
            FROM followers f
            JOIN kols k ON f.user_id = k.user_id
            
            UNION ALL
            
            -- KOL tweet posts
            SELECT 'post', u.user_id, t.tweet_id, t.tweet_id
            FROM user_post_tweet u
            JOIN tweets t ON u.tweet_id = t.tweet_id
            JOIN kols k ON u.user_id = k.user_id
            
            UNION ALL
            
            -- Retweets of KOL tweets
            SELECT 'retweet', r.user_id, upt.user_id, r.tweet_id
            FROM reposts r
            JOIN user_post_tweet upt ON r.tweet_id = upt.tweet_id
            JOIN kols k ON upt.user_id = k.user_id
            
            UNION ALL
            
            -- Comments on KOL tweets
            SELECT 'comment', uct.user_id, t.tweet_id, uct.tweet_id
            FROM user_comment_tweet uct
            JOIN tweets t ON uct.tweet_id = t.tweet_id
            JOIN user_post_tweet upt ON t.tweet_id = upt.tweet_id
            JOIN kols k ON upt.user_id = k.user_id
            
            UNION ALL
            
            -- Mentions
            SELECT 'mention', m.user_id, upt.user_id, m.tweet_id
            FROM mentions m
            JOIN user_post_tweet upt ON m.tweet_id = upt.tweet_id
            JOIN kols k ON upt.user_id = k.user_id
        """)

        for edge_type, source, target, tweet_id in cursor:
            if tweet_id:
                # Add edges through tweet nodes
                self.add_edge(source, tweet_id, edge_type, 'user', 'tweet')
                self.add_edge(tweet_id, target, edge_type, 'tweet', 'user')
            else:
                # Direct user-to-user edge
                self.add_edge(source, target, edge_type)

        cursor.close()
        conn.close()

    def compute_pagerank(self):
        n = len(self.nodes)
        pr = np.ones(n) / n

        # Create weighted adjacency matrix
        adj_matrix = np.zeros((n, n))
        for src, dst, weight, _ in self.edges:
            adj_matrix[dst][src] = weight

        # Normalize by outgoing weights
        out_weights = np.sum(adj_matrix, axis=0)
        adj_matrix = np.divide(adj_matrix, out_weights, where=out_weights!=0)

        for _ in range(self.max_iterations):
            next_pr = np.zeros(n)
            
            # Handle dangling nodes
            dangling_nodes = np.where(out_weights == 0)[0]
            dangling_sum = sum(pr[i] for i in dangling_nodes)

            # Update scores
            for i in range(n):
                incoming = sum(pr[j] * adj_matrix[i][j] for j in range(n))
                next_pr[i] = ((1 - self.damping_factor) / n + 
                             self.damping_factor * (incoming + dangling_sum / n))

            # Check convergence
            if np.sum(np.abs(next_pr - pr)) < self.convergence:
                break

            pr = next_pr

        return pr

    def get_kol_rankings(self):
        scores = self.compute_pagerank()
        
        # Get KOL indices
        kol_nodes = {id: data for id, data in self.nodes.items() 
                    if data['type'] == 'user'}

        # Create rankings list for KOLs only
        rankings = [(node_id, scores[data['index']])
                   for node_id, data in kol_nodes.items()]
        
        return sorted(rankings, key=lambda x: x[1], reverse=True)
    
    # def visualize_graph(self):
    #     import networkx as nx
    #     import matplotlib.pyplot as plt

    #     # Create directed graph
    #     G = nx.DiGraph()

    #     # Add nodes with different colors for users and tweets
    #     for node_id, data in self.nodes.items():
    #         color = 'skyblue' if data['type'] == 'user' else 'lightgreen'
    #         G.add_node(node_id, color=color, type=data['type'])

    #     # Add edges with weights
    #     for src, dst, weight, edge_type in self.edges:
    #         # Convert indices back to node IDs
    #         src_id = [k for k,v in self.nodes.items() if v['index'] == src][0]
    #         dst_id = [k for k,v in self.nodes.items() if v['index'] == dst][0]
    #         G.add_edge(src_id, dst_id, weight=weight, type=edge_type)

    #     # Set up plot
    #     plt.figure(figsize=(15, 10))
    #     pos = nx.spring_layout(G, k=1, iterations=50)

    #     # Draw nodes
    #     node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    #     nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
    #                         node_size=500, alpha=0.7)

    #     # Draw edges with different colors per type
    #     edge_colors = {
    #         'follow': 'gray',
    #         'post': 'green',
    #         'retweet': 'blue',
    #         'comment': 'red',
    #         'mention': 'orange'
    #     }

    #     for edge_type in edge_colors:
    #         edges = [(u, v) for (u, v, d) in G.edges(data=True) 
    #                 if d['type'] == edge_type]
    #         if edges:
    #             nx.draw_networkx_edges(G, pos, edgelist=edges,
    #                                 edge_color=edge_colors[edge_type],
    #                                 arrows=True, arrowsize=10,
    #                                 alpha=0.5, label=edge_type)

    #     # Add labels
    #     labels = {node: str(node)[:10] + '...' if len(str(node)) > 10 
    #             else str(node) for node in G.nodes()}
    #     nx.draw_networkx_labels(G, pos, labels, font_size=8)

    #     plt.title("Twitter Interaction Graph")
    #     plt.legend()
    #     plt.axis('off')
    #     plt.tight_layout()
    #     plt.show()
