var number = document.getElementById('number')
var title = document.getElementById('title')
var body = document.getElementById('body')
var author = document.getElementById('author')
var date = document.getElementById('date')


document.getElementById('saver').onclick = function (){
    var zp = new Object

    zp.id = number.value;
    zp.title = title.value;
    zp.body = body.value
    zp.author = author.value
    zp.date = date.value;   

    archive(zp);
}

function archive(obj){
    // var stringy = JSON.stringify(obj);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", savehandler.py , true); //Замість savehandler.py має бути адреса скрипта який буде зберігати ЗП
    xhr.setRequestHeader('Content-Type', 'application/json' )

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) { 
                document.getElementById("output").innerHTML += xhr.responseText;
            }
        }
    }
    xhr.send(obj);
}