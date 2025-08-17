function createClock() {
    var clockElement = document.createElement("div");
    clockElement.id = "clock";
    clockElement.style.position = "fixed";
    clockElement.style.top = "10px";
    clockElement.style.left = "0";
    clockElement.style.padding = "10px";
    clockElement.style.fontFamily = "Times New Roman, sans-serif";
    clockElement.style.fontSize = "14px";
    clockElement.style.color = "red";
    document.body.appendChild(clockElement);
}

function padZero(number) {
    return number < 10 ? '0' + number : number;
}

function updateClock() {
    var date = new Date();
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var seconds = date.getSeconds();

    var clockElement = document.getElementById("clock");
    if (clockElement) {
        clockElement.textContent = padZero(hours) + ":" + padZero(minutes) + ":" + padZero(seconds);
    }
}

createClock();
setInterval(updateClock, 1000);