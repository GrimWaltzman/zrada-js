var countCom = document.getElementById('count');
var votes = document.getElementsByTagName('select');
var box = document.getElementById('infoblock');
var yes = 0;
var no = 0;
var abs = 0;

countCom.addEventListener('click', function () {
    yes = 0;
    no = 0;
    abs = 0;
    for(var i = 0; i<votes.length;i++){

        if (votes[i].selectedIndex == 1){
            yes++;
        }
        else if (votes[i].selectedIndex == 2){
            no++;
        }
        else if (votes[i].selectedIndex == 3){
            abs++;
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
