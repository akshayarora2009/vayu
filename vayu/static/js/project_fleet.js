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

    $('.btn-ok-data-center-deletion').on("click", function(e){
        deleteDataCenter(data_center_to_del);
    });

    var data_center_to_add_host;
    var $newHostModal = $('#new_host_modal');
    var newHostModalClone = $newHostModal.html();
    $newHostModal.on("hidden.bs.modal", function(ev){
       $newHostModal.html(newHostModalClone);
    });
    $newHostModal.on("shown", function(ev){
       var $invoker = $(ev.relatedTarget);
        data_center_to_add_host = $invoker.attr('data-datacenterid');
    });

    var host_details_known = false;
    $newHostForm = $('#new_host_form');
    var submit_add_new_host_form = function(){
         var loc = window.location.pathname.split("/");
        loc.pop();
        var pathToPost = loc.join("/") + "/host/new";
        $.ajax({
           url: pathToPost,
            method: 'POST',
            data: $newHostForm.serialize() + "&data_center_id=" + data_center_to_add_host + "&host_details=" + host_details_known
        }).done(function(res){
            console.log("Success");
            window.location.reload();
        }).fail(function(err){
            $newHostErrorAlert.show();
            console.log(err);
            $hostErrorList.empty();
            var errors = err.responseJSON.error.errors;
            for(var i = 0; i < errors.length; ++i){
                $hostErrorList.append("<li>" + errors[i] + "</li>");
            }
          window.scrollTo(0, 0);
        });
    };

    $confirmAddHost = $('#confirm_add_host');
    $confirmAddHost.on("click", function(ev){
        ev.preventDefault();
        submit_add_new_host_form();
    });

    $hostErrorList = $('#host_errors');
    $newHostErrorAlert = $('#new_host_error_alert');
    var connectHost = function(){
      $.ajax({
          url: '/hosts/connect',
          method: 'POST',
          data: $newHostForm.serialize()
      }).done(function(res){
          host_details_known = true;
         console.log(res);
      }).fail(function(err){
          $newHostErrorAlert.show();
          console.log(err);
          $hostErrorList.empty();
          var errors = err.responseJSON.error.errors;
          for(var i = 0; i < errors.length; ++i){
              $hostErrorList.append("<li>" + errors[i] + "</li>");
          }
          window.scrollTo(0, 0);
      });
    };

    $newHostForm.on("submit", function(ev){
       ev.preventDefault();
        connectHost();
    });

    hosts = {};
    $newHostModal.on("show.bs.modal", function(ev){
        if($.isEmptyObject(hosts)){
            $.ajax({
                url: '/hosts',
                method: 'GET'
            }).done(function(res){
               console.log(res);
               hosts = res;
            }).fail(function(error){
                console.log(error);
            });
        }
    });

});