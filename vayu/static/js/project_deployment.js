$(function () {

    $.urlParam = function(name){
        var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (results==null){
           return null;
        }
        else{
           return results[1] || 0;
        }
    }

    var startDeployment = (function(){
        var dataString = {};
        dataString["project_id"] = $.urlParam('project_id');
        dataString["project_path"] = "/home/harshita/Documents/test";
        $(".deploy_btn").text("Deploying");
        $(".deploy_btn").append("<img src='../static/img/loading-wheel.gif' id='deploying_gif' style='height:25px;padding-left:10px' alt='...'/>");
        
        $.ajax({
            url: '/abc' ,
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
    })();

    $(".run-button-div").on("click",function(){
        $(".pause-button").show();
        $(".stop-button").show();
        $(this).hide();
    });

    $(".pause-button").on("click",function(){
        $(".play-button").show();
        $(this).hide();
    });

    $(".play-button").on("click",function(){
        $(".pause-button").show();
        $(this).hide();
    });

    $(".stop-button").on("click",function(){
        $(".pause-button").hide();
        $(".play-button").hide();
        $(".run-button-div").show();
        $(this).hide();
    });

    var data = {
        size: 230,
        sectors: [
            {
                percentage: 0.80,
                label: 'Success'
            },
            {
                percentage: 0.15,
                label: "Failure"
            },
            {
                percentage: 0.05,
                label: "Error"
            }
        ]
    }

    function calculateSectors( data ) {
        var sectors = [];
        var colors = [
            "#21ab21","red","grey"
        ];

        var l = data.size / 2
        var a = 0 // Angle
        var aRad = 0 // Angle in Rad
        var z = 0 // Size z
        var x = 0 // Side x
        var y = 0 // Side y
        var X = 0 // SVG X coordinate
        var Y = 0 // SVG Y coordinate
        var R = 0 // Rotation


        data.sectors.map( function(item, key ) {
            a = 360 * item.percentage;
            aCalc = ( a > 180 ) ? 360 - a : a;
            aRad = aCalc * Math.PI / 180;
            z = Math.sqrt( 2*l*l - ( 2*l*l*Math.cos(aRad) ) );
            if( aCalc <= 90 ) {
                x = l*Math.sin(aRad);
            }
            else {
                x = l*Math.sin((180 - aCalc) * Math.PI/180 );
            }
            
            y = Math.sqrt( z*z - x*x );
            Y = y;

            if( a <= 180 ) {
                X = l + x;
                arcSweep = 0;
            }
            else {
                X = l - x;
                arcSweep = 1;
            }

            sectors.push({
                percentage: item.percentage,
                label: item.label,
                color: colors[key],
                arcSweep: arcSweep,
                L: l,
                X: X,
                Y: Y,
                R: R
            });

            R = R + a;
        })


        return sectors
    }

    sectors = calculateSectors(data);
    var newSVG = document.createElementNS( "http://www.w3.org/2000/svg","svg" );
    newSVG.setAttributeNS(null, 'style', "width: "+data.size+"px; height: " + data.size+ "px");
    document.getElementById("project_statistics").appendChild(newSVG)


    sectors.map( function(sector) {

        var newSector = document.createElementNS( "http://www.w3.org/2000/svg","path" );
        newSector.setAttributeNS(null, 'fill', sector.color);
        newSector.setAttributeNS(null, 'd', 'M' + sector.L + ',' + sector.L + ' L' + sector.L + ',0 A' + sector.L + ',' + sector.L + ' 0 ' + sector.arcSweep + ',1 ' + sector.X + ', ' + sector.Y + ' z');
        newSector.setAttributeNS(null, 'transform', 'rotate(' + sector.R + ', '+ sector.L+', '+ sector.L+')');

        newSVG.appendChild(newSector);
    })

    var midCircle = document.createElementNS( "http://www.w3.org/2000/svg","circle" );
    midCircle.setAttributeNS(null, 'cx', data.size * 0.5 );
    midCircle.setAttributeNS(null, 'cy', data.size * 0.5);
    midCircle.setAttributeNS(null, 'r', data.size * 0.28 );
    midCircle.setAttributeNS(null, 'fill', '#42495B' );

    newSVG.appendChild(midCircle);

});