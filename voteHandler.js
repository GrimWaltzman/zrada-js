var countCom = document.getElementById('count');
var votes = document.getElementsByTagName('select');
var box = document.getElementById('infoblock');
var yes = 0;
var no = 0;
var abs = 0;
var boxes = document.getElementsByClassName('checkbox');

document.body.addEventListener('click', function(e){
    if(e.target.getAttribute('class')=='checkbox'){
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
                break;
            case 'against':
                no++;
                break;
            case 'abstained':
                abs++;
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
    }
    else {
        document.getElementById('verdict').innerHTML = 'Рішення не прийнято'
    }
}

