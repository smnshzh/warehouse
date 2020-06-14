function box_getter(number) {
    var productName = document.getElementById("product_name" + number);
    var _valuePn = productName.value;
    var inBox = productDictBox[_valuePn];

    var quantityBox = document.getElementById("product_box_quantity" + number);

    var quantituQyantity = document.getElementById("product_quantity" + number);

    quantituQyantity.value = Number(quantityBox.value) * Number(inBox)

}


function warehouse_getter() {

    var hiddenUsername = document.getElementById("username");
    var warehouseselect = document.getElementById("warehouse");
    var warehouseList = accessDict[hiddenUsername.value].warehouse;

    for (var m = 0; m < warehouseList.length; m++) {

        if (!document.getElementById(warehouseList[m])) {
            var craeted_nod_option = document.createElement("option");
            craeted_nod_option.id = warehouseList[m];
            craeted_nod_option.value = warehouseList[m];
            craeted_nod_option.innerHTML = warehouseList[m];
            warehouseselect.append(craeted_nod_option);

        }
    }
};


function active_sending() {
    var listOfSelectedProducts = [];
    var suplier = document.getElementById("suplier");
    var product = document.getElementsByClassName("product_name");

    var sending = document.getElementById("sending");
    var productLen = product.length;
    var quantity = document.getElementsByClassName("product_quantity");

    var quantityListSelect = [];
    for (var l = 0; l < quantity.length; l++) {
        quantityListSelect.push(quantity[l].value)
    }
    var price = document.getElementsByClassName("buy_price");

    var priceListSelect = [];
    for (var h = 0; h < price.length; h++) {
        priceListSelect.push(price[h].value)
    }



    var listTrue = 0;

    for (var i = 0; i < productLen; i++) {


        if (productsList.includes(product[i].value)) {

            listTrue++;

        }

    }
    for (var d = 0; d < product.length; d++) {
        if (listOfSelectedProducts.includes(product[d].value)) {
            (product[d]).style.borderColor = 'red';
        } else {
            listOfSelectedProducts.push(product[d].value);
            (product[d]).style.borderColor = 'white';

        }
    }

    var totalPrice = document.getElementsByClassName("total_price");
    var totalPriceList = [];

    for (var k = 0;k < totalPrice.length;k++ ){
        totalPriceList.push(totalPrice[k].value)

    }

    sending.disabled = !(accountsideList.includes(suplier.value) && listTrue === productLen
        && !quantityListSelect.includes('0')
        && !quantityListSelect.includes("")
        && !priceListSelect.includes("0")
        && !priceListSelect.includes("")
        && !quantityListSelect.includes(0)
        && !priceListSelect.includes(0)
        && !totalPriceList.includes("NaN")
        && !totalPriceList.includes("0")
        && !totalPriceList.includes(0));
}


function return_sumOfTotalPrice() {


    var tpClass = document.getElementsByClassName("total_price");
    var sumTotalPrice = Number(0);
    for (var i = 0; i < tpClass.length; i++) {
        sumTotalPrice += Number(tpClass[i].value);
        document.getElementById("som_of_total_price").innerHTML = sumTotalPrice
    }
}


function price_getter(number) {


    box_getter(number);

    active_sending();


    var productSelectId = "product_name" + number;

    var productSelect = document.getElementById("product_name" + number);
    var productVat = document.getElementById("vat" + number);
    var productSelectValue = productSelect.value;
    var offTag = document.getElementById("product_off" + number);
    // var price = document.getElementById('price' + number);
    var priceElement = document.getElementById("price" + number);


    var totalPriceElement = document.getElementById("total_Price" + number);
    var quantityElement = document.getElementById("product_quantity" + number);
    var quantityElementValue = parseInt(quantityElement.value);





    if (priceElement.value !== undefined) {

        var final_price_sell_order = parseFloat( priceElement.value) * ((100.00 - parseFloat(offTag.value)) / 100) * ((100.00 + parseFloat(productVat.value)) / 100) * Number(quantityElementValue);
        totalPriceElement.value = final_price_sell_order.toFixed(2)
    } else {
        priceElement.value = "";
        totalPriceElement.value = "";


        //}


        //{#console.log(productSelectValue);#}
        //{#console.log(price);#}
    }

    return_sumOfTotalPrice();
}


function append_input() {
    var productClass = document.getElementsByClassName('product_name');
    var quantityClass = document.getElementsByClassName('product_quantity');
    var priceClass = document.getElementsByClassName("buy_price");

    if ((productClass[Number(productClass.length) - Number(1)].value) &&
        quantityClass[Number(quantityClass.length) - Number(1)].value &&
        priceClass[Number(priceClass.length) - Number(1)].value

    ) {


        var number = (document.getElementsByClassName('product_name')).length;
        var productListCount = productsList.length;
        var inputNumber = Number(number) + Number(1);
        if (number < productListCount) {
            var node = document.getElementById('product');
            var tr_node = document.createElement("tr");
            tr_node.id = toString(inputNumber);
            tr_node.className = "TR";
            node.append(tr_node);
            var td_node_product = document.createElement('td');
            var td_nod_box = document.createElement('td');
            var td_nod_quantity = document.createElement('td');
            var td_node_price = document.createElement('td');
            var td_node_off = document.createElement('td');
            var td_node_vat = document.createElement('td');
            var td_node_tPrice = document.createElement('td');
            tr_node.append(td_node_product);
            tr_node.append(td_nod_box);
            tr_node.append(td_nod_quantity);
            tr_node.append(td_node_price);
            tr_node.append(td_node_off);
            tr_node.append(td_node_vat);
            tr_node.append(td_node_tPrice);

            var created_nod_product = document.createElement('input');
            var created_nod_box = document.createElement('input');
            var created_nod_quntity = document.createElement('input');
            var created_nod_price = document.createElement('input');
            var created_nod_off = document.createElement('input');
            var created_nod_vat = document.createElement('input');
            var created_nod_tPrice = document.createElement('input');

            created_nod_product.type = 'text';
            created_nod_product.className = 'product_name input-group-text';
            created_nod_product.placeholder = "Product Name" + inputNumber;
            created_nod_product.name = "product_name" + inputNumber;
            created_nod_product.id = "product_name" + inputNumber;
            created_nod_product.required = true;


            created_nod_box.type = 'number';
            created_nod_box.className = 'product_box_quantity input-group-text';
            created_nod_box.placeholder = "Quantity" + inputNumber;
            created_nod_box.name = "product_name" + inputNumber;
            created_nod_box.id = "product_box_quantity" + inputNumber;
            created_nod_box.required = true;
            created_nod_box.min = "1";


            created_nod_quntity.type = 'number';
            created_nod_quntity.className = 'product_quantity input-group-text';
            created_nod_quntity.placeholder = "Quantity" + inputNumber;
            created_nod_quntity.name = "product_name" + inputNumber;
            created_nod_quntity.id = "product_quantity" + inputNumber;
            created_nod_quntity.min = "1";
            created_nod_quntity.disabled = true;


            created_nod_price.id = "price" + inputNumber;
            created_nod_price.type = 'number';
            created_nod_price.step = "0.01";
            created_nod_price.className = "buy_price input-group-text";
            created_nod_price.name = "product_name" + inputNumber;
            created_nod_price.min = "1";


            created_nod_off.type = 'number';
            created_nod_off.className = 'product_off input-group-text';
            created_nod_off.placeholder = "";
            created_nod_off.name = "product_name" + inputNumber;
            created_nod_off.id = "product_off" + inputNumber;
            created_nod_off.required = false;
            created_nod_off.min = "0";


            created_nod_vat.type = 'number';
            created_nod_vat.className = 'vat input-group-text';
            created_nod_vat.placeholder = "";
            created_nod_vat.name = "product_name" + inputNumber;
            created_nod_vat.id = "vat" + inputNumber;
            created_nod_vat.required = false;
            created_nod_vat.min = "0";

            created_nod_tPrice.id = "total_Price" + inputNumber;
            created_nod_tPrice.type = "number";
            created_nod_tPrice.disabled = true;
            created_nod_tPrice.className = "total_price input-group-text";


            td_node_product.append(created_nod_product);
            td_nod_box.append(created_nod_box);
            td_nod_quantity.append(created_nod_quntity);
            td_node_off.append(created_nod_off);
            td_node_vat.append(created_nod_vat);
            td_node_price.append(created_nod_price);
            td_node_tPrice.append(created_nod_tPrice);

            created_nod_product.addEventListener("keyup", function () {
                price_getter(inputNumber)
            });

            created_nod_price.addEventListener("keyup", function () {
                price_getter(inputNumber)
            });

            created_nod_box.addEventListener("keyup", function () {
                price_getter(inputNumber)
            });

            created_nod_vat.addEventListener("keyup", function () {
                price_getter(inputNumber)

            });

            $(".product_name").autocomplete({
                source: productsList

            })
        } else {
            alert('You Can not make input mor than products')
        }

    } else {
        alert("Complet last filled")
    }
    active_sending();
}
// function append_input() {
//     var productClass = document.getElementsByClassName('product_name');
//     var quantityClass = document.getElementsByClassName('product_quantity');
//     var priceClass = document.getElementsByClassName("buy_price");
//
//     if ((productClass[Number(productClass.length) - Number(1)].value)
//         && quantityClass[Number(quantityClass.length) - Number(1)].value
//         && priceClass[Number(priceClass.length) - Number(1)].value
//
//     ) {
//
//
//         var number = (document.getElementsByClassName('product_name')).length;
//         var productListCount = productsList.length;
//         var inputNumber = Number(number) + Number(1);
//         if (number < productListCount) {
//             var node = document.getElementById('product');
//             var tr_node = document.createElement("tr");
//             tr_node.id = toString(inputNumber);
//             tr_node.className = "TR";
//             node.append(tr_node);
//             var td_node_product = document.createElement('td');
//             var td_nod_box = document.createElement('td');
//             var td_node_quantity = document.createElement('td');
//             var td_node_price = document.createElement('td');
//             var td_node_tPrice = document.createElement('td');
//             tr_node.append(td_node_product);
//             tr_node.append(td_nod_box);
//             tr_node.append(td_node_quantity);
//             tr_node.append(td_node_price);
//             tr_node.append(td_node_tPrice);
//             var created_nod_product = document.createElement('input');
//             var created_nod_box = document.createElement('input');
//             var created_nod_quntity = document.createElement('input');
//             var created_nod_price = document.createElement('input');
//             var created_nod_tPrice = document.createElement('input');
//
//             created_nod_product.type = 'text';
//             created_nod_product.className = 'product_name input-group-text';
//             created_nod_product.placeholder = "Product Name" + inputNumber;
//             created_nod_product.name = "product_name" + inputNumber;
//             created_nod_product.id = "product_name" + inputNumber;
//             created_nod_product.required = true;
//
//             created_nod_box.type = 'number';
//             created_nod_box.className = 'product_box_quantity input-group-text';
//             created_nod_box.placeholder = "Quantity" + inputNumber;
//             created_nod_box.name = "product_name" + inputNumber;
//             created_nod_box.id = "product_box_quantity" + inputNumber;
//             created_nod_box.required = true;
//             created_nod_box.min = "1";
//
//             created_nod_quntity.type = 'number';
//             created_nod_quntity.className = 'product_quantity input-group-text';
//             created_nod_quntity.placeholder = "Quantity" + inputNumber;
//             created_nod_quntity.name = "product_name" + inputNumber;
//             created_nod_quntity.id = "product_quantity" + inputNumber;
//             created_nod_quntity.required = true;
//             created_nod_quntity.min = "1";
//             created_nod_quntity.disabled = true;
//
//             created_nod_price.id = "price" + inputNumber;
//             created_nod_price.type = 'number';
//             created_nod_price.step = "0.01";
//             created_nod_price.className = "buy_price input-group-text";
//             created_nod_price.name = "product_name" + inputNumber;
//             created_nod_price.min = "1";
//
//             created_nod_tPrice.id = "total_Price" + inputNumber;
//             created_nod_tPrice.disabled = true;
//             created_nod_tPrice.className = "total_price input-group-text";
//
//
//             td_node_product.append(created_nod_product);
//             td_nod_box.append(created_nod_box);
//             td_node_quantity.append(created_nod_quntity);
//             td_node_price.append(created_nod_price);
//             td_node_tPrice.append(created_nod_tPrice);
//
//             created_nod_product.addEventListener("keyup" && "click", function () {
//                 price_getter(inputNumber)
//             });
//             created_nod_quntity.addEventListener("keyup" && "click", function () {
//                 price_getter(inputNumber)
//             });
//
//             created_nod_price.addEventListener("keyup", function () {
//                 price_getter(inputNumber)
//             });
//
//             created_nod_price.addEventListener("click", function () {
//                 price_getter(inputNumber)
//             });
//
//             created_nod_box.addEventListener("keyup", function () {
//                 price_getter(inputNumber)
//             });
//
//
//             $(".product_name").autocomplete({
//                 source: productsList
//
//             })
//         } else {
//             alert('You Can not make input mor than products')
//         }
//
//     } else {
//         alert("Complet last filled")
//     }
//     active_sending();
// }

function remove_input() {
    var trClass = document.getElementsByClassName('TR');

    if (Number(trClass.length) > 1) {
        (trClass[Number(trClass.length) - Number(1)]).remove()

    }
    active_sending()

}

function accountside_info() {
    var suplierValue = document.getElementById('suplier').value;
    var accountSideInfoList = accountsideDict[suplierValue];
    var accountsideID = document.getElementById('id');
    var accountsideName = document.getElementById('name');
    var accountsideTel = document.getElementById('Tel');
    var accountsideAddress = document.getElementById("address");
    var hiddenInput = document.getElementById("customer_id");
    if (accountSideInfoList) {
        accountsideID.innerHTML = accountSideInfoList.id;
        accountsideName.innerHTML = accountSideInfoList.name;
        accountsideTel.innerHTML = accountSideInfoList.telephonnumber;
        accountsideAddress.innerHTML = accountSideInfoList.region_city + ' - ' + accountSideInfoList.region_local_name + ' - ' + accountSideInfoList.address;
        hiddenInput.value = accountSideInfoList.id;
    } else {
        accountsideID.innerHTML = "";
        accountsideName.innerHTML = "";
        accountsideTel.innerHTML = "";
        accountsideAddress.innerHTML = "";
    }
    active_sending()
}


