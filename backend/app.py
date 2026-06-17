from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
#cpu调度模块
# =========================
#1.FCFS 算法
# =========================

@app.route('/scheduler/fcfs', methods=['POST'])
def fcfs():
    data = request.json
    processes = data['processes']
    # 按到达时间排序
    processes.sort(key=lambda x: x['arrival'])
    current_time = 0
    gantt = []
    results = []
    for p in processes:
        if current_time < p['arrival']:
            current_time = p['arrival']
        start = current_time
        end = start + p['burst']
        finish = end
        turnaround = finish - p['arrival']
        weighted = round(turnaround / p['burst'], 2)
        gantt.append({
            "pid": p['pid'],
            "start": start,
            "end": end
        })
        results.append({
            "pid": p['pid'],
            "finish": finish,
            "turnaround": turnaround,
            "weighted": weighted
        })
        current_time = end
    return jsonify({
        "gantt": gantt,
        "results": results
    })


# =========================
#2.RR时间片轮转
# =========================

@app.route('/scheduler/rr', methods=['POST'])
def rr():

    data = request.json
    processes = data['processes']
    tq = data.get("time_slice", 2)

    queue = processes[:]
    time = 0

    gantt = []

    remain = {p['pid']: p['burst'] for p in processes}
    arrival = {p['pid']: p['arrival'] for p in processes}

    completion = {p['pid']: 0 for p in processes}

    ready = []
    finished = set()

    while len(finished) < len(processes):

        for p in queue:
            if p['arrival'] <= time and p not in ready and p['pid'] not in finished:
                ready.append(p)

        if not ready:
            time += 1
            continue

        p = ready.pop(0)
        pid = p['pid']

        run_time = min(tq, remain[pid])

        start = time
        time += run_time
        end = time

        gantt.append({
            "pid": pid,
            "start": start,
            "end": end
        })

        remain[pid] -= run_time

        if remain[pid] == 0:
            finished.add(pid)
            completion[pid] = time
        else:
            ready.append(p)

    results = []

    for p in processes:

        pid = p['pid']
        arrival_time = p['arrival']
        burst = p['burst']
        finish = completion[pid]

        turnaround = finish - arrival_time
        weighted = round(turnaround / burst, 2)

        results.append({
            "pid": pid,
            "finish": finish,
            "turnaround": turnaround,
            "weighted": weighted
        })

    return jsonify({
        "gantt": gantt,
        "results": results
    })


# =========================
#3.抢占式
# =========================
@app.route('/scheduler/sjf', methods=['POST'])
def sjf():

    data = request.json
    processes = data['processes']

    time = 0
    gantt = []

    remain = {p['pid']: p['burst'] for p in processes}
    arrival = {p['pid']: p['arrival'] for p in processes}

    completion = {p['pid']: 0 for p in processes}

    finished = set()

    while len(finished) < len(processes):

        ready = [p for p in processes if p['arrival'] <= time and p['pid'] not in finished]

        if not ready:
            time += 1
            continue

        p = min(ready, key=lambda x: remain[x['pid']])
        pid = p['pid']

        start = time
        time += 1
        end = time

        gantt.append({
            "pid": pid,
            "start": start,
            "end": end
        })

        remain[pid] -= 1

        if remain[pid] == 0:
            finished.add(pid)
            completion[pid] = time

    # ===== 结果计算 =====
    results = []

    for p in processes:

        pid = p['pid']
        arrival_time = p['arrival']
        burst = p['burst']
        finish = completion[pid]

        turnaround = finish - arrival_time
        weighted = round(turnaround / burst, 2)

        results.append({
            "pid": pid,
            "finish": finish,
            "turnaround": turnaround,
            "weighted": weighted
        })

    return jsonify({
        "gantt": gantt,
        "results": results
    })


# =========================
#4.HRN
# =========================
@app.route('/scheduler/hrn', methods=['POST'])
def hrn():

    data = request.json
    processes = data['processes']

    # 复制进程数据
    procs = []
    for p in processes:
        procs.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "remaining": p["burst"],
            "start": None,
            "finish": None
        })

    time = 0
    finished = 0
    n = len(procs)

    gantt = []
    results = []

    while finished < n:

        # 找已到达且未完成的进程
        ready = [p for p in procs if p["arrival"] <= time and p["remaining"] > 0]

        if not ready:
            time += 1
            continue

        # 计算响应比
        def response_ratio(p):
            waiting = time - p["arrival"]
            return (waiting + p["burst"]) / p["burst"]

        # 选择响应比最大的
        current = max(ready, key=response_ratio)

        # 执行（HRN是非抢占，一次执行完）
        start = time
        end = time + current["remaining"]

        current["start"] = start
        current["finish"] = end

        gantt.append({
            "pid": current["pid"],
            "start": start,
            "end": end
        })

        time = end
        current["remaining"] = 0
        finished += 1

        turnaround = current["finish"] - current["arrival"]
        weighted = round(turnaround / current["burst"], 2)

        results.append({
            "pid": current["pid"],
            "finish": current["finish"],
            "turnaround": turnaround,
            "weighted": weighted
        })

    return jsonify({
        "gantt": gantt,
        "results": results
    })

# =========================
# 启动
# =========================

if __name__ == '__main__':
    app.run(debug=True)