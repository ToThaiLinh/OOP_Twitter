import pandas as pd

# Dữ liệu ví dụ
data = {
    'follower_user_id': [123, 789, 101, 131],
    'kol_user_id': [456, 456, 112, 112]
}

df = pd.DataFrame(data)

import networkx as nx
import matplotlib.pyplot as plt

# Tạo đồ thị có hướng
G = nx.DiGraph()

# Thêm các cặp follower và KOL vào đồ thị
for index, row in df.iterrows():
    G.add_edge(row['follower_user_id'], row['kol_user_id'])

# Vẽ đồ thị
plt.figure(figsize=(8, 6))

# Tùy chọn vị trí các node
pos = nx.spring_layout(G)

# Vẽ các node (người dùng)
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue', alpha=0.8)

# Vẽ các cạnh có hướng (hướng từ follower đến KOL)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle='->', arrowsize=20, edge_color='gray')

# Thêm nhãn cho các node
nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

# Hiển thị đồ thị
plt.title("Đồ thị hướng từ người theo dõi đến người được theo dõi")
plt.axis('off')  # Tắt hiển thị trục
plt.show()
