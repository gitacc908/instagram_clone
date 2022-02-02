$(function(){
const users_div_desktop = $('#search-res-desktop')
const res_content = $('#res-content')
const user_input_desktop = $('#input-btn-desktop')
const endpoint = $("#input-btn-desktop").attr('data-search-url')
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            res_content.fadeTo('slow', 0).promise().then(() => {
                    users_div_desktop.html(response['html_from_view'])
                    res_content.fadeTo('slow', 1)
                })
       
        })
}
// desktop search event
user_input_desktop.on('keyup', function (event) {
    var val = user_input_desktop.val()
    if (val.charAt(0)=='#'){
        var request_parameters = {
            q: $(this).val(),
            desktop: true,
            hashtag: true
        }
    }
    else{
        var request_parameters = {
            q: $(this).val(),
            desktop: true
        }
    }
    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})
});