from flask import Flask, request, jsonify
from flask_cors import CORS
from algorithms.scheduler import scheduler_bp
from algorithms.producer_consumer import producer_consumer_bp
app = Flask(__name__)
CORS(app)


app.register_blueprint(
    scheduler_bp
)
app.register_blueprint(
    producer_consumer_bp
)
# =========================
# 启动
# =========================

if __name__ == '__main__':
    app.run(debug=True)