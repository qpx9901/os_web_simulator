from flask import Blueprint
from flask import request
from flask import jsonify

producer_consumer_bp = Blueprint(
    "producer_consumer",
    __name__
)


@producer_consumer_bp.route(
    "/producer_consumer/run",
    methods=["POST"]
)
def run_simulation():
    data = request.json
    buffer_size = int(data.get("buffer_size", 10))
    producer_count = int(
        data.get("producer_count", 2)
    )
    consumer_count = int(
        data.get("consumer_count", 2)
    )
    consume_n = int(
        data.get("consume_n", 2)
    )
    steps = int(
        data.get("steps", 20)
    )
    buffer = [0] * buffer_size
    count = 0
    history = []
    producer_index = 0
    consumer_index = 0
    for step in range(steps):
        # 生产阶段
        if step % 2 == 0:
            if count < buffer_size:
                buffer[count] = 1
                count += 1
                producer_id = (
                    producer_index % producer_count
                ) + 1
                producer_index += 1
                history.append({
                    "action":
                        f"Producer {producer_id} Produce",
                    "buffer":
                        buffer.copy(),
                    "type":
                        "produce"
                })
        # 消费阶段
        else:
            if count >= consume_n:
                consumer_id = (
                    consumer_index % consumer_count
                ) + 1
                consumer_index += 1
                for _ in range(consume_n):
                    count -= 1
                    buffer[count] = 0
                history.append({
                    "action":
                        f"Consumer {consumer_id} Consume {consume_n}",
                    "buffer":
                        buffer.copy(),
                    "type":
                        "consume"
                })
    return jsonify({
        "history": history
    })