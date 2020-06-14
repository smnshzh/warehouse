var productoffxmlhttp = new XMLHttpRequest();
var url5 = "http://127.0.0.1:8000/rfw/productoff/";

var productOffDict = {};
var productOffList = [];
productoffxmlhttp.open("GET", url5, true);
productoffxmlhttp.send();
productoffxmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var productoff = JSON.parse(this.response);

        for (let i = 0; i < productoff.length; i++) {
            productOffDict[productoff[i].name] = productoff[i]

        }
    }
};


var productxmlhttp = new XMLHttpRequest();
var url1 = "http://127.0.0.1:8000/rfw/product/";
var productDict = {};
var productDictPrice = {};
var productDictBox = {};
const productsList = [];
productxmlhttp.open("GET", url1, true);
productxmlhttp.send();
productxmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        let product = JSON.parse(this.responseText);
        for (let i = 0; i < product.length; i++) {
            productDict[product[i].name] = product[i];
            productDictPrice[product[i].name] = product[i].price;
            productDictBox[product[i].name] = product[i].box;
            productsList.push(product[i].name);
        }

    }

};

var accountsidexmlhttp = new XMLHttpRequest();
var url2 = "http://127.0.0.1:8000/rfw/accountside/";

var accountsideDict = {};
var accountsideNameList = [];
var accountsideList = [];
accountsidexmlhttp.open("GET", url2, true);
accountsidexmlhttp.send();
accountsidexmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var accountside = JSON.parse(this.response);
        for (let i = 0; i < accountside.length; i++) {
            accountsideList.push(accountside[i].id_code + "-" + accountside[i].name);
            accountsideDict[accountside[i].id_code + "-" + accountside[i].name] = accountside[i];
            accountsideNameList.push(accountside[i].name);

        }


    }

};

var userxmlhttp = new XMLHttpRequest();
var url3 = "http://127.0.0.1:8000/rfw/users/";

var userDict = {};
var userList = [];
userxmlhttp.open("GET", url3, true);
userxmlhttp.send();
userxmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var user = JSON.parse(this.response);
        for (let i = 0; i < user.length; i++) {
            userList.push(user[i].first_name + " " + user[i].last_name);

            userDict[user[i].first_name + " " + user[i].last_name] = user[i];
        }

    }

};


var orderitemxmlhttp = new XMLHttpRequest();
var url4 = "http://127.0.0.1:8000/rfw/orderitems/";

var orderitemDict = {};
var orderitemList = [];
orderitemxmlhttp.open("GET", url4, true);
orderitemxmlhttp.send();
orderitemxmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var orderitem = JSON.parse(this.response);

        for (let i = 0; i < orderitem.length; i++) {
            if (orderitemDict[orderitem[i].shipment_id]) {
                var existed_key = Number(orderitemDict[orderitem[i].shipment_id]);
                existed_key += Number(orderitem[i].total_price);
            } else {
                orderitemDict[orderitem[i].shipment_id] = Number(orderitem[i].total_price);

            }
            shipmentFinalPriceClass = document.getElementsByClassName('shipment_final_price');
            for (var k = 0; k < shipmentFinalPriceClass.length; k++) {

                var selected_tag = shipmentFinalPriceClass[k];
                var id = shipmentFinalPriceClass[k].id;
                selected_tag.innerHTML = orderitemDict[id];
            }
        }
    }

};


var warehousexmlhttp = new XMLHttpRequest();
var url6 = "http://127.0.0.1:8000/rfw/users/";
var warehouseDict = {};
var warehouseList = [];
warehousexmlhttp.open("GET", url6, true);
warehousexmlhttp.send();
warehousexmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var warehouse = JSON.parse(this.response);
        for (let i = 0; i < warehouse.length; i++) {
            warehouseList.push(warehouse[i].name);
            warehouseDict[warehouse[i].name] = warehouse[i];
        }

    }

};


var accessxmlhttp = new XMLHttpRequest();
var url7 = "http://127.0.0.1:8000/rfw/access/";
var accessDict = {};
var accessList = [];
accessxmlhttp.open("GET", url7, true);
accessxmlhttp.send();
accessxmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var access = JSON.parse(this.response);
        for (let i = 0; i < access.length; i++) {
            accessList.push(access[i].user_username);
            accessDict[access[i].user_username] = access[i];
        }

    }

};

var difintxmlhttp = new XMLHttpRequest();
var url8 = "http://127.0.0.1:8000/rfw/definitAccount/";
var difintDict = {};
var difintList = [];
difintxmlhttp.open("GET", url8, true);
difintxmlhttp.send();
difintxmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var difint = JSON.parse(this.response);
        for (let i = 0; i < difint.length; i++) {
            difintList.push(difint[i].code +'-'+ difint[i].name);
        }

    }

};