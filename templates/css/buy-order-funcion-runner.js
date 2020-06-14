document.addEventListener("mousemove", function () {
    accountside_info();
    var classname = document.getElementsByClassName("TR");
    for (var i = 1; i < classname.length + 1; i++) {
        price_getter(i)
    }
});