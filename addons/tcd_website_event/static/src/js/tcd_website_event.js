$(document).ready(function () {
        $('input:radio[name=answer]').change(function () {
            console.log("changed!");
            if ($("input[name='answer']:checked").val() == '2') {
                $("#invitee_guest").slideDown(500);
            }
            if ($("input[name='answer']:checked").val() != '2') {
                $("#invitee_guest").slideUp(500);
            }
        });
    });