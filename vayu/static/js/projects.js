$(function () {
    var deployButton;
    $('.hide-start').hide();
    var submit_form = function(){
        $.ajax({
            url: '/projects/new',
            method: 'POST',
            data: $newProjectForm.serialize()
        }).done(function(res){
            location.reload();
        }).fail(function(error){

            $('#add_new_error_alert').show();
            var res = error.responseJSON;
            $addErrors = $('#add_new_errors');
            $addErrors.empty();
            var errors = res.error.errors;
            for(var i = 0; i < errors.length; ++i){
                $addErrors.append("<li>" + errors[i] + "</li>");
            }
        });
    };
    $newProjectForm = $('#new_project_form');
    $newProjectForm.on('submit', submit_form);
    $('#add_project_btn').on('click', submit_form);

    var deleteProject = function(project_id){
        var dataString = "project_id=" + project_id;
        $.ajax({
            url: '/projects/delete',
            method: 'POST',
            data: dataString
        }).done(function(res){
            console.log(res);
            window.location.reload();
        }).fail(function(error){
            alert("Something went wrong");
        })
    };

    $confirmDelete = $('#confirm-delete');

    $delProject = $('.delete_project');

    var project_to_delete;
    $delProject.on("click", function(ev){
        project_to_delete = $(this).attr('data-id');
        $confirmDelete.modal();
    });

    $('.btn-ok').on("click", function (e) {
       deleteProject(project_to_delete);
    });

    $('.manage_project').on("click", function(e){
       e.preventDefault();
        window.location.href("/projects/" + $(this).attr('data-target'));
    });

    function get_uuid() {
      function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
          .toString(16)
          .substring(1);
      }
      return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
        s4() + '-' + s4() + s4() + s4();
    }

    var deployProject = function (project_id , project_path , uuid) {
        var dataString = {};
        dataString["project_id"] = project_id;
        dataString["project_path"] = project_path;
        $.ajax({
            url: '/' + uuid,
            method: 'POST',
            data: dataString
        }).done(function(res){
            console.log(res);
            deployButton.text("Deployed");
            $("#deploying_gif").remove();
        }).fail(function(error){
            alert("Something went wrong");
        })
    };

    $('.deploy').on("click",function (e) {
        e.preventDefault();
        console.log("1111");
        deployButton = $(this);
        var key = $(this).data("key"),
            path = $(this).data("path"),
            uuid = get_uuid();
        $(this).text("Deploying");
        $(this).append("<img src='../static/img/loading-wheel.gif' id='deploying_gif' style='height:25px;padding-left:10px' alt='...'/>");
        deployProject(key , path , uuid);
    })

});