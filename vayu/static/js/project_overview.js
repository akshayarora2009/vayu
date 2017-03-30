$(function(){

    var $language_version_label = $("#language_version_label"),
    $language_version_id = $("#language_version_id"),
    $language_prod_label = $("#language_prod_label"),
    $language_prod_id = $("#language_prod_id"),
    $deployment_language_id = $("#deployment_language_id"),
    $overview_form = $("#overview_form"),
    deployButton;

    var language = {
            "Node.js" : {
                versions : [ "7.x" , "6.x" , "5.x" , "4.x" , "3.x"],
                production : [ "pm2" , "forever"]
            },
            "Java" : {
                versions : [ "1.7" , "1.6" , "1.5" , "1.4"]
            },
            "Android" : { 
                versions : [ "7.x" , "6.x" , "5.x" , "4.x" , "3.x" , "2.x" ]
            }
    };

    var fillLanguageVersion = function(){
        var selected_language = $("#deployment_language_id option:selected").val();
        var versions = language[selected_language].versions;
        $language_version_label.empty();
        $language_version_label.append('<label> Select ' + selected_language + ' version</label>');
        $language_version_id.empty();
        $.each(versions, function(index, value) {
            $language_version_id.append('<option>' + value + '</option>');
        });
    };

    var fillProductionVersion = function(){
        var selected_language = $("#deployment_language_id option:selected").val();
        var production = language[selected_language].production;
        $language_prod_label.empty();
        $language_prod_label.append('<label> Select ' + selected_language + ' production version</label>');
        $language_prod_id.empty();
        $.each(production, function(index, value) {
            $language_prod_id.append('<option>' + value + '</option>');
        });
    };

    var createLanguageDropdown = (function(){
        var language_key = [];
        for(var key in language) 
            language_key.push(key);
        $.each(language_key, function(index, value) {
            $deployment_language_id.append('<option>' + value + '</option>');
        });
        fillLanguageVersion();
        fillProductionVersion();
    })();
    
    $deployment_language_id.on("change",function(e){
        e.preventDefault();
        fillLanguageVersion();
        fillProductionVersion();
    });

    var get_uuid =function() {
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
        }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
    };

    $overview_form.on("submit", function(e){
        e.preventDefault();
        // var project_id = $(".start_deployment_btn").data("id");
        var project_id = $(location).attr("href").split('/')[4];
        var dataString = $overview_form.serialize() + "&project_id=" + project_id;
        var uuid = get_uuid();
        window.location.href = "/deployments/" + uuid + "?" + dataString;   
    });

});