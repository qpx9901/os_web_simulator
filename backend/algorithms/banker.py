from flask import Blueprint, request, jsonify

banker_bp = Blueprint('banker', __name__)

# =========================
# 银行家算法核心逻辑
# =========================
def banker_algorithm(allocation, max_need, available):

    n = len(allocation)
    m = len(available)

    # 计算 Need
    need = [
        [max_need[i][j] - allocation[i][j] for j in range(m)]
        for i in range(n)
    ]

    work = available[:]
    finish = [False] * n
    safe_sequence = []

    changed = True

    while len(safe_sequence) < n and changed:
        changed = False

        for i in range(n):
            if not finish[i]:

                can_run = True
                for j in range(m):
                    if need[i][j] > work[j]:
                        can_run = False
                        break

                if can_run:
                    for j in range(m):
                        work[j] += allocation[i][j]

                    finish[i] = True
                    safe_sequence.append(i)
                    changed = True

    safe = len(safe_sequence) == n

    return {
        "gantt": [],
        "results": [],
        "safe": safe,
        "sequence": safe_sequence
    }


# =========================
# Flask API接口
# =========================
@banker_bp.route('/banker', methods=['POST'])
def banker():

    data = request.json

    allocation = data["allocation"]
    max_need = data["max_need"]
    available = data["available"]

    result = banker_algorithm(allocation, max_need, available)

    return jsonify(result)