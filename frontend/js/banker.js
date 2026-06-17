async function runBanker() {

    const allocation = JSON.parse(document.getElementById("allocation").value);
    const max_need = JSON.parse(document.getElementById("maxNeed").value);
    const available = JSON.parse(document.getElementById("available").value);

    const res = await fetch("http://127.0.0.1:5000/banker", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            allocation,
            max_need,
            available
        })
    });

    const data = await res.json();

    renderResult(data);
}

function renderResult(data) {

    const statusDiv = document.getElementById("status");
    const table = document.getElementById("resultTable");

    table.innerHTML = `
        <tr>
            <th>安全序列</th>
        </tr>
    `;

    if (data.safe) {

        statusDiv.innerHTML = `<h3 class="safe">系统安全</h3>`;

        table.innerHTML += `
            <tr>
                <td>${data.sequence.join(" → ")}</td>
            </tr>
        `;

    } else {

        statusDiv.innerHTML = `<h3 class="unsafe">系统不安全</h3>`;

        table.innerHTML += `
            <tr>
                <td>无安全序列</td>
            </tr>
        `;
    }
}