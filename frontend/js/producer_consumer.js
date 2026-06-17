let historyData = [];

let currentStep = 0;

let speed = 500;


async function runSimulation(){

    currentStep = 0;

    speed =
        parseInt(
            document.getElementById(
                "speed"
            ).value
        );

    const data = {

        buffer_size:
            parseInt(
                document.getElementById(
                    "bufferSize"
                ).value
            ),

        producer_count:
            parseInt(
                document.getElementById(
                    "producerCount"
                ).value
            ),

        consumer_count:
            parseInt(
                document.getElementById(
                    "consumerCount"
                ).value
            ),

        consume_n:
            parseInt(
                document.getElementById(
                    "consumeN"
                ).value
            ),

        steps:
            parseInt(
                document.getElementById(
                    "steps"
                ).value
            )
    };

    const response = await fetch(

        "http://127.0.0.1:5000/producer_consumer/run",

        {
            method:"POST",

            headers:{
                "Content-Type":
                    "application/json"
            },

            body:
                JSON.stringify(data)
        }
    );

    const result =
        await response.json();

    historyData =
        result.history;

    document.getElementById(
        "log"
    ).innerHTML = "";

    playAnimation();
}


function playAnimation(){

    if(
        currentStep >=
        historyData.length
    ){
        return;
    }

    const item =
        historyData[currentStep];

    renderBuffer(
        item.buffer,
        item.type
    );

    addLog(
        item.action
    );

    currentStep++;

    setTimeout(
        playAnimation,
        speed
    );
}


function renderBuffer(
    buffer,
    type
){

    const area =
        document.getElementById(
            "bufferArea"
        );

    area.innerHTML = "";

    buffer.forEach(value=>{

        const div =
            document.createElement(
                "div"
            );

        div.classList.add(
            "cell"
        );

        if(value===1){

            div.classList.add(
                "full"
            );

            div.innerText="1";

        }else{

            div.classList.add(
                "empty"
            );

            div.innerText="0";
        }

        area.appendChild(
            div
        );
    });
}


function addLog(text){

    const log =
        document.getElementById(
            "log"
        );

    log.innerHTML +=
        text + "<br>";

    log.scrollTop =
        log.scrollHeight;
}