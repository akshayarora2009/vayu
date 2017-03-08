$(function () {

    var submit_form = function(){
        $.ajax({
            url: '/projects/new',
            method: 'POST',
            data: $newProjectForm.serialize()
        }).done(function(res){
            alert('sent');
        }).fail(function(error){
            alert('error');
        });
    };
    $newProjectForm = $('#new_project_form');
    $newProjectForm.on('submit', submit_form);
    $('#add_project_btn').on('click', submit_form);
});