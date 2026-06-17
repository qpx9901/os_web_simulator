async function run() {

    const requests = document.getElementById("requests").value
        .split(",")
        .map(x => parseInt(x.trim()));

    const head = parseInt(document.getElementById("head").value);
    const algo = document.getElementById("algo").value;

    const res = await fetch("http://127.0.0.1:5000/disk", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            requests,
            head,
            algo
        })
    });

    const data = await res.json();

    render(data);
}

function render(data) {

    const track = document.getElementById("track");
    track.innerHTML = "";

    data.gantt.forEach(g => {

        const div = document.createElement("div");
        div.className = "block";
        div.innerText = g.pos;

        track.appendChild(div);
    });

    document.getElementById("total").innerHTML =
        "总寻道长度：" + data.total_seek;
}