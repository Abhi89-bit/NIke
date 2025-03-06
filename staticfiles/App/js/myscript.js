document.addEventListener("DOMContentLoaded", function() {
    $('.plus-cart').click(function() {
        var id = $(this).attr('id'); 
        var a = this.parentNode.children[2]; 
        console.log('id: ', id);
        $.ajax({
            type: 'GET',
            url: "/plus-cart",
            data: { prod_id: id },
            success: function(data){
                console.log("data: ", data);
                a.innerText = data.quantity; // Corrected innertext to innerText
                document.getElementById("amount").innerHTML = data.amount;
                document.getElementById("total").innerHTML = data.total;
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    $('.minus-cart').click(function() {
        var id = $(this).attr('id'); 
        var a = this.parentNode.children[2]; 
        console.log('id: ', id);
        $.ajax({
            type: 'GET',
            url: "/minus-cart",
            data: { prod_id: id },
            success: function(data){
                console.log("data: ", data);
                a.innerText = data.quantity; // Corrected innertext to innerText
                document.getElementById("amount").innerHTML = data.amount;
                document.getElementById("total").innerHTML = data.total;
            }
        });
    });
});


