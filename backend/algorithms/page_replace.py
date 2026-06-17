from flask import Blueprint, request, jsonify

page_bp = Blueprint('page', __name__)

# =========================
# FIFO
# =========================
def fifo(pages, frames):
    memory = []
    queue = []
    faults = 0
    detail = []

    for p in pages:
        hit = p in memory

        if not hit:
            faults += 1

            if len(memory) < frames:
                memory.append(p)
                queue.append(p)
            else:
                old = queue.pop(0)
                idx = memory.index(old)
                memory[idx] = p
                queue.append(p)

        detail.append({
            "page": p,
            "memory": memory[:],
            "hit": hit
        })

    return faults, detail


# =========================
# LRU
# =========================
def lru(pages, frames):
    memory = []
    last_used = {}
    faults = 0
    detail = []

    for i, p in enumerate(pages):
        hit = p in memory

        if hit:
            last_used[p] = i
        else:
            faults += 1

            if len(memory) < frames:
                memory.append(p)
            else:
                lru_page = min(memory, key=lambda x: last_used[x])
                memory[memory.index(lru_page)] = p

            last_used[p] = i

        detail.append({
            "page": p,
            "memory": memory[:],
            "hit": hit
        })

    return faults, detail


# =========================
# OPT
# =========================
def opt(pages, frames):
    memory = []
    faults = 0
    detail = []

    for i in range(len(pages)):
        p = pages[i]
        hit = p in memory

        if not hit:
            faults += 1

            if len(memory) < frames:
                memory.append(p)
            else:
                farthest = -1
                replace_idx = 0

                for j in range(len(memory)):
                    try:
                        next_use = pages[i+1:].index(memory[j])
                    except:
                        next_use = float('inf')

                    if next_use > farthest:
                        farthest = next_use
                        replace_idx = j

                memory[replace_idx] = p

        detail.append({
            "page": p,
            "memory": memory[:],
            "hit": hit
        })

    return faults, detail


# =========================
# API接口
# =========================
@page_bp.route('/page', methods=['POST'])
def page_replace_api():

    data = request.json
    pages = data["pages"]
    frames = data["frames"]
    algo = data.get("algo", "fifo")

    if algo == "fifo":
        faults, detail = fifo(pages, frames)
    elif algo == "lru":
        faults, detail = lru(pages, frames)
    else:
        faults, detail = opt(pages, frames)

    return jsonify({
        "gantt": [],
        "results": [],
        "faults": faults,
        "detail": detail
    })