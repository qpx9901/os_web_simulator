from flask import Flask, request, jsonify
from flask_cors import CORS
from algorithms.scheduler import scheduler_bp
from algorithms.producer_consumer import producer_consumer_bp
from algorithms.banker import banker_bp
from algorithms.page_replace import page_bp
from algorithms.disk_schedule import disk_bp

app = Flask(__name__)
#CORS(app)
CORS(app, supports_credentials=True)

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