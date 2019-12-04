var main = document.getElementById('main');
  main.onclick = function(e){
    if(e.target.tagName == 'BUTTON')
    deleter(e.target.getAttribute("data-id"))
  }

  function deleter(id){

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "" , true); //кинеш куди тобі треба
    xhr.setRequestHeader('Content-Type', 'text/plain' );

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) { 
                console.log(xhr.responseText);
            }
        }
    };
    xhr.send(id);
}