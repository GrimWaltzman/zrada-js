var main = document.getElementById('main');
  main.onclick = function(e){
    if(e.target.tagName == 'BUTTON')
    deleter(e.target.getAttribute("data-id"))
  }

  function deleter(id){

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/law_del" , true); //кинеш куди тобі треба
    xhr.setRequestHeader('Content-Type', 'application/json' );

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) { 
                console.log(xhr.responseText);
            }
        }
    };
    post = new Object;
    post._id = id;
    post_json = JSON.stringify(post);
    xhr.send(post_json);
}