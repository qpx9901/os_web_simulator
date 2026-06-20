import os
from flask import Flask, request, jsonify
from flask import send_from_directory
from flask_cors import CORS
from algorithms.scheduler import scheduler_bp
from algorithms.producer_consumer import producer_consumer_bp
from algorithms.banker import banker_bp
from algorithms.page_replace import page_bp
from algorithms.disk_schedule import disk_bp

#CORS(app)
app = Flask(__name__)
CORS(app, supports_credentials=True)


BASE_DIR=os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR=os.path.join(BASE_DIR,"../frontend")
#前端托管，可以直接通过ipv4地址访问该网站页面，也可以继续点击index.html
@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR,"index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR,path)

@app.route("/")
def index():
    return {
        "project":"OS Web Simulator",
        "status":"running"
    }





app.register_blueprint(scheduler_bp)
app.register_blueprint(producer_consumer_bp)
app.register_blueprint(banker_bp)
app.register_blueprint(page_bp)
app.register_blueprint(disk_bp)
# =========================
# 启动
# =========================

if __name__ == '__main__':
    app.run(debug=True)