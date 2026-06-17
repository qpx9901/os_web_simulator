async function run() {

    const pages = document.getElementById("pages").value
        .split(",")
        .map(x => parseInt(x.trim()));

    const frames = parseInt(document.getElementById("frames").value);

    const algo = document.getElementById("algo").value;

    const res = await fetch("http://127.0.0.1:5000/page", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            pages,
            frames,
            algo
        })
    });

    const data = await res.json();

    render(data);
}

function render(data) {

    document.getElementById("faults").innerHTML =
        `<h2>${data.faults}</h2>`;

    let table = document.getElementById("table");

    table.innerHTML = `
        <tr>
            <th>页面</th>
            <th>内存状态</th>
            <th>是否命中</th>
        </tr>
    `;

    data.detail.forEach(d => {

        table.innerHTML += `
            <tr>
                <td>${d.page}</td>
                <td>${d.memory.join(",")}</td>
                <td class="${d.hit ? 'hit' : 'fault'}">
                    ${d.hit ? '命中' : '缺页'}
                </td>
            </tr>
        `;
    });
}