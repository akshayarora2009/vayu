$(function () {
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
            location.reload();
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


});