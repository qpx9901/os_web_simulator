function addProcess() {

    const table = document.getElementById("processTable");

    const row = table.insertRow();

    row.innerHTML = `
        <td><input value="P"></td>
        <td><input value="0"></td>
        <td><input value="1"></td>
    `;
}

async function run() {

    const algo = document.getElementById("algo").value;
    const timeSlice = parseInt(document.getElementById("timeSlice").value || 2);

    const table = document.getElementById("processTable");

    let processes = [];

    for (let i = 1; i < table.rows.length; i++) {

        const cells = table.rows[i].cells;

        processes.push({
            pid: cells[0].children[0].value,
            arrival: parseInt(cells[1].children[0].value),
            burst: parseInt(cells[2].children[0].value)
        });
    }

    let url = "http://127.0.0.1:5000/scheduler/" + algo;

    let body = { processes };

    if (algo === "rr") {
        body.time_slice = timeSlice;
    }

    const res = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    const data = await res.json();

    renderResult(data.results || []);
    renderGantt(data.gantt || []);
}

function renderResult(results) {

    const table = document.getElementById("resultTable");

    table.innerHTML = `
        <tr>
            <th>PID</th>
            <th>完成时间</th>
            <th>周转时间</th>
            <th>带权周转时间</th>
        </tr>
    `;

    results.forEach(r => {

        table.innerHTML += `
            <tr>
                <td>${r.pid}</td>
                <td>${r.finish}</td>
                <td>${r.turnaround}</td>
                <td>${r.weighted}</td>
            </tr>
        `;
    });
}

function renderGantt(gantt) {

    const div = document.getElementById("gantt");

    div.innerHTML = "";

    let scale = 40;

    gantt.forEach(g => {

        const block = document.createElement("div");

        block.className = "block";

        block.style.width = (g.end - g.start) * scale + "px";

        block.innerHTML = `${g.pid}`;

        div.appendChild(block);
    });
}