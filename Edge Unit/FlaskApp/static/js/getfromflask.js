var person_name = ""
var time = ""
var dept = ""
var date = ""
var gate = ""
var pervious_person_name = ""
var pervious_time = ""
var tablebody = document.getElementById("dataTable")

function httpGet(theUrl) {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText
}


setInterval(function () {
    let pageurl = window.location.href;
    let buffer = JSON.parse(httpGet(pageurl + "recognized"));
    console.log(buffer)

    if (buffer['name'] != "Empty") {


        person_name = buffer['name']
        time = buffer['time']
        dept = buffer['Department']
        date = buffer['date']
        gate = buffer['Gate']

        if (person_name != pervious_person_name && time != pervious_time) {
            tablebody.innerHTML += `<tr><td>${person_name}</td><td>${time}</td><td>${dept}</td><td>${gate}</td><td>${date}</td></tr>`
            pervious_person_name = person_name
            pervious_time = time
        }
    }
}, 300);