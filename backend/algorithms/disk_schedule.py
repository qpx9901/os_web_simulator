from flask import Blueprint, request, jsonify

disk_bp = Blueprint('disk', __name__)

# =========================
# SSTF
# =========================
def sstf(req, head):

    req = req[:]
    current = head
    gantt = [{"pos": head}]
    total = 0

    while req:

        closest = min(req, key=lambda x: abs(x - current))
        total += abs(closest - current)
        current = closest

        gantt.append({"pos": current})
        req.remove(closest)

    return gantt, total


# =========================
# SCAN
# =========================
def scan(req, head, direction):

    req = sorted(req)
    current = head
    gantt = []
    total = 0

    left = [r for r in req if r < head]
    right = [r for r in req if r >= head]

    if direction == "right":

        for r in right:
            total += abs(r - current)
            current = r
            gantt.append({"pos": current})

        for r in reversed(left):
            total += abs(r - current)
            current = r
            gantt.append({"pos": current})

    else:

        for r in reversed(left):
            total += abs(r - current)
            current = r
            gantt.append({"pos": current})

        for r in right:
            total += abs(r - current)
            current = r
            gantt.append({"pos": current})

    return [{"pos": head}] + gantt, total


# =========================
# C-SCAN
# =========================
def cscan(req, head):

    req = sorted(req)
    current = head
    gantt = [{"pos": head}]
    total = 0

    right = [r for r in req if r >= head]
    left = [r for r in req if r < head]

    for r in right:
        total += abs(r - current)
        current = r
        gantt.append({"pos": current})

    if left:
        # 回到起点（模拟磁道0 -> max）
        total += abs(current - 0)
        total += abs(req[-1] - 0)

        current = 0

        for r in left:
            total += abs(r - current)
            current = r
            gantt.append({"pos": current})

    return gantt, total


# =========================
# API
# =========================
@disk_bp.route('/disk', methods=['POST'])
def disk_schedule():

    data = request.json
    req = data["requests"]
    head = data["head"]
    algo = data.get("algo", "sstf")
    direction = data.get("direction", "right")

    if algo == "sstf":
        gantt, total = sstf(req, head)
    elif algo == "scan":
        gantt, total = scan(req, head, direction)
    else:
        gantt, total = cscan(req, head)

    return jsonify({
        "gantt": gantt,
        "results": [],
        "total_seek": total
    })