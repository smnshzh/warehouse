


setInterval(timeFunc, 1000)

function timeFunc() {
    let d = new Date
    document.getElementById('time').innerHTML = d.toLocaleTimeString()
}






function outOfOrder(classname) {

    stocks = document.getElementsByClassName(classname);


    for (var i = 0; i < stocks.length; i++) {
        var inner = stocks[i].innerHTML;


        if (Number(inner) < 60) {

            stocks[i].style.color = 'red';
        }
    }
}


function add(){
   var $new_input=document.createElement( "input" )
    let new_p=document.createElement("p")

    $( " .input" ).append( new_p,$new_input );
}


