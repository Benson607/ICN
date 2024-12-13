from http.server import HTTPServer, SimpleHTTPRequestHandler

class CustomHandler(SimpleHTTPRequestHandler):
    # 重写默认的 MIME 类型映射
    extensions_map = {
        '.html': 'text/html',
        '.htm': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',  # 修正 .js 的 MIME 类型
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.txt': 'text/plain',
        '.svg': 'image/svg+xml',
        '': 'application/octet-stream',  # 默认类型
    }

if __name__ == "__main__":
    server_address = ('', 8000)  # 监听所有接口，端口8000
    httpd = HTTPServer(server_address, CustomHandler)
    print("Serving on port 8000...")
    httpd.serve_forever()