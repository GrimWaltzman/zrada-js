var number = document.getElementById('number')
var title = document.getElementById('title')
var body = document.getElementById('body')
var author = document.getElementById('author')
var date = document.getElementById('date')


document.getElementById('saver').onclick = function (){
    var zp = new Object

    zp.id = number.value;
    zp.title = title.value;
    zp.body = body.value;
    zp.author = author.value;
    zp.date = date.value;   
    
    console.log(zp);

    archive(zp);
}

function archive(obj){
     var xhr = new XMLHttpRequest();
     xhr.open("POST", "/insert_law" , true); //Замість savehandler.py має бути адреса скрипта який буде зберігати ЗП

     xhr.onreadystatechange = function () {
         if (xhr.readyState == 4) {
             if (xhr.status == 200) { 
                 document.getElementById("output").innerHTML += xhr.responseText;
             }
         }
     }

     xhr.send(obj);
 }
