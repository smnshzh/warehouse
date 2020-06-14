function display_block(num) {


    table_get = document.getElementsByClassName("hidden" + num);

    for (var l = 0; l < table_get.length; l++) {

        if (table_get[l].style.display === "none") {
            table_get[l].style.display = ""
        } else {
            table_get[l].style.display = "none"
        }
    }
}


function false_color(num) {
var poseItem = document.getElementById("settle"+num);
    if (poseItem.style.backgroundColor !== "red"){
    poseItem.style.backgroundColor = "red";
    poseItem.style.color= "white";}
    else {
        poseItem.style.backgroundColor = "";
        poseItem.style.color = "black";
    }
}

function confirm_color(num) {
var poseItem = document.getElementById("settle"+num);
    if (poseItem.style.backgroundColor !== "red"){
    poseItem.style.backgroundColor = "green";
    poseItem.style.color= "white";}
    else {
        poseItem.style.backgroundColor = "";
        poseItem.style.color = "black";
    }
}