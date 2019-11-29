var countCom = document.getElementById('count');
var votes = document.getElementsByTagName('select');
var box = document.getElementById('infoblock');
var yes = 0;
var no = 0;
var abs = 0;
var boxes = document.getElementsByClassName('checkbox mx-auto');
var selector = document.getElementById('lawid');
var result = {
    yes:[],
    no: [],
    abstained: [],
}

selector.onchange = function(){
    result.lawIndex = selector.selectedIndex;
}

document.body.addEventListener('click', function(e){
    if(e.target.getAttribute('class')=='checkbox mx-auto'){
        switch(e.target.getAttribute('data-vote')){
            case 'none':
                e.target.setAttribute('data-vote', 'for');
                break;
            case 'for':
                e.target.setAttribute('data-vote', 'against')
                break;
            case 'against':
                e.target.setAttribute('data-vote', 'abstained');
                break;
            case 'abstained':
                e.target.setAttribute('data-vote', 'for');
                break;
        }
    }

})

countCom.addEventListener('click', function () {
    yes = 0;
    no = 0;
    abs = 0;
    for(var i = 0; i<boxes.length;i++){
        var vote = boxes[i].getAttribute('data-vote');
        switch(vote){
            case 'for':
                yes++;
                result.yes.push(boxes[i].getAttribute('data-name'));
                break;
            case 'against':
                no++;
                result.no.push(boxes[i].getAttribute('data-name'));
                break;
            case 'abstained':
                abs++;
                result.abstained.push(boxes[i].getAttribute('data-name'));
                break;
        }
    }
    display();
});

function display(){
    if(yes+no+abs<10){
        alert("Вкажіть всі голоси");
    }
    else{
        var pro = document.getElementById('pro');
        pro.innerHTML = "За: "+ yes;
        var con = document.getElementById('con');
        con.innerHTML = "Проти: "+ no;
        var ind = document.getElementById('ind');
        ind.innerHTML = "Утрималися: "+ abs;

        verdictCounter();
    }
}

function verdictCounter (){
    if (yes>=(no+abs)){
        document.getElementById('verdict').innerHTML = 'Рішення прийнято'
        result.verdict = "Прийнято";
    }
    else {
        document.getElementById('verdict').innerHTML = 'Рішення не прийнято'
        result.verdict = "Не прийнято";
    }
    console.log(result);
    sendRequest();
}

function sendRequest(){
    var xhr = new XMLHttpRequest();

    var final = JSON.stringify(result);

    xhr.open("POST", "/creator");

    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log(xhr.responseText);
        }
    }

    xhr.send(final);
}




