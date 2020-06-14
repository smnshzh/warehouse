document.addEventListener("mousemove", function () {
    accountside_info();
    get_visitor_id();
    var classname = document.getElementsByClassName("TR");
    console.log(classname.length);
    for (var i = 1; i < classname.length + 1; i++) {
        price_getter(i)
    }
});