$(function(){
   $('.hide-start').hide();

    $newDataCenterForm = $('#new_data_center_form');

    var submitForm = function(){
        var loc = window.location.pathname.split("/");
        loc.pop();
        var pathToPost = loc.join("/") + "/new-data-center";
        $.ajax({
            url: pathToPost,
            method: 'POST',
            data: $newDataCenterForm.serialize()
        }).done(function(res){
            location.reload()
        }).fail(function(error){
            $('#add_new_error_alert').show();
            var res = error.responsJSON;
            $addErrors = $('#add_new_errors');
            $addErrors.empty();
            var errors = res.error.errors;
            for(var i = 0; i < errors.length; ++i){
                $addErrors.append("<li>" + errors[i] + "</li>");
            }
        });
    };

    var deleteDataCenter = function(data_center_id){
        var dataString = "data_center_id=" + data_center_id;
        var loc = window.location.pathname.split("/");
        loc.pop();
        var pathToPost = loc.join("/") + "/delete-data-center";
        $.ajax({
            url: pathToPost,
            method: 'POST',
            data: dataString
        }).done(function(res){
           location.reload();
        }).fail(function(error){
            alert("Something went wrong");
        });
    };

    $newDataCenterForm.on("submit", submitForm);
    $('#add_data_center_btn').on("click", submitForm);


    $delDataCenter = $('.delete-data-center');
    $confirmDelete = $('#confirm-delete');

    var data_center_to_del;
    $delDataCenter.on("click", function(ev){
       ev.preventDefault();
        data_center_to_del = $(this).attr('data-id');
        $confirmDelete.modal();
    });

    $('.btn-ok').on("click", function(e){
        deleteDataCenter(data_center_to_del);
    });

});