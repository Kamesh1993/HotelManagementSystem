// DatePicker
$(function () {
    var $dp1 = $("#datepicker_CIn");
    $dp1.datepicker({
        changeMonth: true,
        changeYear: true,
        minDate: 0
    });
    var $dp2 = $("#datepicker_COut");
    $dp2.datepicker({
        changeMonth: true,
        minDate: 0
    });
    $("#datepicker_CIn").datepicker();
    $("#datepicker_COut").datepicker();
    //Pass the user selected date format
    $("#format").change(function () {
        $("#datepicker_CIn").datepicker("option", "dateFormat: 'yyyy-mm-dd'", $(this).val());
        $("#datepicker_COut").datepicker("option", "dateFormat: 'yyyy-mm-dd'", $(this).val());
    });
});
function handler(e) {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!
    var yyyy = today.getFullYear();
    today = mm + '/' + dd + '/' + yyyy;
    selected = e.target.value;
    if (selected > today) {
        alert("please selected above today date");
        $('#datepicker_CIn').val('');
        $('#datepicker_COut').val('');
    }
}
function date(f) {
    var cin = document.getElementById("datepicker_CIn").value;
    var cout = document.getElementById("datepicker_COut").value;
    if (cout < cin) {
        alert("Check out date cannot be less than check in date");
        $('#datepicker_COut').val('');
    }
}