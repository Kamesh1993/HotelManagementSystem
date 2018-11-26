// DatePicker
$(function ()
{
    $("#datepicker_CIn").datepicker();
    $("#datepicker_COut").datepicker();
    //Pass the user selected date format
    $("#format").change(function ()
    {
        $("#datepicker_CIn").datepicker("option", "dateFormat", $(this).val());
        $("#datepicker_COut").datepicker("option", "dateFormat", $(this).val());
    });
});

function handler(e)
{
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!
    var yyyy = today.getFullYear();
    today = mm + '/' + dd + '/' + yyyy;
    if (selected < today)
    {
        alert("Please check the dates you mentioned");
        $('#datepicker_CIn').val('');
        $('#datepicker_COut').val('');
    }
}   