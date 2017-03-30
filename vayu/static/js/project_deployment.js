$(function () {

    $.urlParam = function(name){
        var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (results==null){
           return null;
        }
        else{
           return results[1] || 0;
        }
    };

    var nextDeployment = function (dataString) {
        var project_id = dataString["project_id"];
        $.ajax({
            url: '/deploy/' + project_id ,
            method: 'POST',
            data: dataString
        }).done(function(res){
            console.log(res);
            $(".deploy_btn").text("Deployed");
            $("#deploying_gif").remove();
        }).fail(function(error){
            alert("Something went wrong");
            $(".deploy_btn").text("Deployment failed");
            $("#deploying_gif").remove();
        })
    };

    var startDeployment = (function(){
        var dataString = {},
            project_id = $.urlParam('project_id'),
            entryPoint = $.urlParam('entry_point');
        dataString["project_id"] = project_id;
        dataString["entry_point"] = entryPoint;
        $.ajax({
            url: '/api/projects/' + project_id ,
            method: 'GET',
            data: dataString
        }).done(function(res){
            $(".deploy_btn").text("Deploying");
            $(".deploy_btn").append("<img src='../static/img/loading-wheel.gif' id='deploying_gif' style='height:25px;padding-left:10px' alt='...'/>");
            var data = res.data[0];
            dataString["project_path"] = data.path;
            dataString["git_ignore"] = data.use_gitignore;
            nextDeployment(dataString);
        }).fail(function(error){
            alert("Something went wrong");
        });
    })();

});