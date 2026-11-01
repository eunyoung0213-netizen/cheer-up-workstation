import os
import random
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

# 설정은 코드에 박지 않고 환경 변수로 받는다 (없으면 기본값 사용)
PORT = int(os.environ.get("PORT", "5000"))
APP_MODE = os.environ.get("APP_MODE", "dev")

MESSAGES = [
    "천천히 가도 괜찮아요. 멈추지만 않으면 돼요.",
    "터미널을 열어 본 것만으로도 큰 한 걸음이에요.",
    "오류는 실패가 아니라 단서예요.",
    "모르는 게 당연해요. 처음이니까요.",
    "한 줄씩 하다 보면 어느새 다 와 있어요.",
]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 컨테이너가 살아 있는지 확인하는 주소
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"ok")
            return

        message = random.choice(MESSAGES)
        host = socket.gethostname()  # 컨테이너 안에서는 컨테이너 ID가 나온다
        html = (
            "<html><head><meta charset='utf-8'><title>Cheer Up</title></head>"
            "<body style='font-family:sans-serif;text-align:center;margin-top:80px'>"
            "<h1>오늘의 응원</h1>"
            f"<p style='font-size:24px'>{message}</p>"
            "<hr>"
            f"<small>컨테이너: {host} / 모드: {APP_MODE} / 컨테이너 포트: {PORT}</small>"
            "</body></html>"
        )
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"서버 시작: 포트 {PORT}, 모드 {APP_MODE}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
