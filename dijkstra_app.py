from flask import Flask, request, jsonify, render_template
import heapq

# ----- Đồ thị như bài Dijkstra kinh điển -----
graph = {
    0: {1: 4, 7: 8},
    1: {0: 4, 2: 8, 7: 11},
    2: {1: 8, 3: 7, 8: 2, 5: 4},
    3: {2: 7, 4: 9, 5: 14},
    4: {3: 9, 5: 10},
    5: {2: 4, 3: 14, 4: 10, 6: 2},
    6: {5: 2, 7: 1, 8: 6},
    7: {0: 8, 1: 11, 6: 1, 8: 7},
    8: {2: 2, 6: 6, 7: 7},
}

# ----- Thuật toán Dijkstra (giữ nguyên style của bạn) -----
def dijkstra(graph, s, t):
    # dist[v]: độ dài đường đi tốt nhất hiện tại từ s đến v
    dist = {v: float("inf") for v in graph}
    # prev[v]: đỉnh đứng trước v trên đường đi ngắn nhất
    prev = {v: None for v in graph}

    dist[s] = 0
    pq = [(0, s)]       # priority queue: (khoảng cách, đỉnh)
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        if u == t:
            break

        for v, w in graph[u].items():
            if v in visited:
                continue
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    # Dựng lại đường đi
    if dist[t] == float("inf"):
        return float("inf"), []

    path = []
    cur = t
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return dist[t], path


# ----- Tạo Flask app -----
app = Flask(__name__)

def _build_edges(g):
    """Chuyển adjacency dict thành danh sách cạnh không có trùng (vì đồ thị vô hướng)."""
    seen = set()
    edges = []
    for u, nbrs in g.items():
        for v, w in nbrs.items():
            key = (min(u, v), max(u, v))
            if key in seen:
                continue
            seen.add(key)
            edges.append({"source": key[0], "target": key[1], "weight": w})
    return edges


@app.route("/")
def home():
    # Trang chủ: render template có trực quan đồ thị + form chọn src/dst
    nodes = sorted(graph.keys())
    edges = _build_edges(graph)
    return render_template("index.html", nodes=nodes, edges=edges, graph=graph)


@app.route("/api/graph")
def api_graph():
    nodes = sorted(graph.keys())
    edges = _build_edges(graph)
    return jsonify(nodes=nodes, edges=edges)

@app.route("/api/shortest-path")
def api_shortest_path():
    # Lấy tham số từ URL: /api/shortest-path?src=0&dst=4
    try:
        src = int(request.args.get("src", 0))
        dst = int(request.args.get("dst", 4))
    except ValueError:
        return jsonify(error="src và dst phải là số nguyên"), 400

    if src not in graph or dst not in graph:
        return jsonify(error="src/dst không tồn tại trong đồ thị"), 400

    dist, path = dijkstra(graph, src, dst)
    if dist == float("inf"):
        return jsonify(distance=-1, path=[])

    return jsonify(distance=dist, path=path)

@app.route("/result")
def show_result():
    # Trang HTML hiển thị kết quả cho form ở "/"
    try:
        src = int(request.args.get("src", 0))
        dst = int(request.args.get("dst", 4))
    except ValueError:
        return "<p>src/dst phải là số nguyên.</p>"

    if src not in graph or dst not in graph:
        return "<p>src/dst không tồn tại trong đồ thị.</p>"

    dist, path = dijkstra(graph, src, dst)
    if dist == float("inf"):
        return f"<p>Không có đường đi từ {src} đến {dst}.</p>"

    path_str = " -> ".join(map(str, path))
    return f"""
    <h3>Kết quả Dijkstra</h3>
    <p>Đường đi ngắn nhất từ {src} đến {dst}: <b>{path_str}</b></p>
    <p>Độ dài: <b>{dist}</b></p>
    <p><a href="/">Quay lại</a></p>
    """

if __name__ == "__main__":
    # Chạy server Flask
    app.run(debug=True, port=5050)