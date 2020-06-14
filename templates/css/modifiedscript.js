function final_price_sum() {


        var totalPriceClass = document.getElementsByClassName("total_price");
        var finalPrice = document.getElementById("final");
        var total = parseFloat("0");
        for (var i = 0; i < totalPriceClass.length; i++) {
            var totalValue = totalPriceClass[i].innerHTML;
            total += parseFloat(totalValue)

        }
        finalPrice.innerHTML = total.toFixed(2);
    }

        final_price_sum();
    document.addEventListener("keyup", function () {
        final_price_sum()

    });