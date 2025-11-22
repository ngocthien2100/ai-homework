# Dijkstra Flask Demo (Visualizer)

Một giao diện trực quan để thử thuật toán Dijkstra trên đồ thị mẫu.

## Cách chạy

```zsh
# Từ thư mục dự án
'/Users/ngocthien/ai-notebooks/ai-venv/bin/python' python_app.py
```

Mở trình duyệt: http://127.0.0.1:5050

## API
- Tính đường đi ngắn nhất: `GET /api/shortest-path?src=<int>&dst=<int>`

Ví dụ:
```zsh
curl 'http://127.0.0.1:5050/api/shortest-path?src=0&dst=4'
```

## Giao diện
- Chọn nguồn/đích và bấm "Tính đường đi".
- Đường đi ngắn nhất sẽ được highlight (vàng) trên đồ thị.
- Có nút Đổi (swap) và Xóa highlight.

Thư viện sử dụng trên client: Bootstrap 5 (CDN) và Cytoscape.js (CDN).
