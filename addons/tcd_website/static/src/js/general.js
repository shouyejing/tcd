$(document).ready(function () {
/*
        $("#output").pivot(
            [
                {color: "blue", shape: "circle"},
                {color: "red", shape: "triangle"}
            ],
            {
                rows: ["color"],
                cols: ["shape"]
            }
        );
*/
     setTimeout(function() {
         if($(".oe_currency_value").length > 0) {
             $(".oe_currency_value").html($(".oe_currency_value").html().slice(0,-3));
         }
         if($(".noindex").length > 0) {
             $("head").append('<meta name="robots" content="noindex, nofollow"/>')
        }
         if($("#product_detail").length > 0 || $("#catalog-form").length > 0) {
            url = $("span[itemprop='url']").html();
            window.history.pushState(history.state, "Good deal", url);
        }
    }, 100);

    $('.o_website_form_send').click(function(e) {
        console.log("button-clicked");
        if ($("input[name='general_conditions_accepted']").length > 0) {
            if (!$("input[name='general_conditions_accepted']").is(":checked")) {
                console.log("submit stopped");
                e.preventDefault();
                alert("Please accept our general conditions");
            }
        }
    })
});
