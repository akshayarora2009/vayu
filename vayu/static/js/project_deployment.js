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

    var startDeployment = function (dataString) {
        var project_id = dataString["project_id"];
        $.ajax({
            url: '/deploy/' + project_id ,
            method: 'POST',
            data: dataString
        }).done(function(res){
            // console.log(res);
            // $(".deploy_btn").text("Deployed");
            // $("#deploying_gif").remove();
        }).fail(function(error){
            alert("Something went wrong");
            $(".deploy_btn").text("Deployment failed");
            $("#deploying_gif").remove();
        })
    };

    var getHostDetails = (function(){
        var dataString = {},
            deployment_language = $.urlParam('deployment_language'),
            project_id = $.urlParam('project_id'),
            entryPoint = $.urlParam('entry_point'),
            port_number = $.urlParam('port_number'),
            project_path = $.urlParam('project_path'),
            git_ignore = $.urlParam('git_ignore');

            dataString["deployment_language"] = deployment_language;
            dataString["project_id"] = project_id;
            dataString["entry_point"] = entryPoint;
            dataString["port_number"] = port_number;
            dataString["project_path"] = project_path;
            dataString["git_ignore"] = git_ignore;

            console.log(JSON.stringify(dataString));

            $(".deploy_btn").text("Deploying");
            $(".deploy_btn").append("<img src='../static/img/loading-wheel.gif' id='deploying_gif' style='height:25px;padding-left:10px' alt='...'/>");
            
            $.ajax({
                url: '/api/projects/' + project_id ,
                method: 'GET'
            }).done(function(res){
                var data = res.data[0],
                    fleet = data.host_details;
                for (var key in fleet){
                    host = key
                    user = fleet[key].host_auth_user;
                    password = fleet[key].host_auth_password;

                    break;
                }
                dataString["host"] = host;
                dataString["user"] = user;
                dataString["password"] = password;
                console.log(JSON.stringify(dataString));
            }).fail(function(error){
                alert("Something went wrong");
            });
            startDeployment(dataString);
    })();

});