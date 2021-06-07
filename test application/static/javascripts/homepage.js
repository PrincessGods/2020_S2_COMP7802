//window width
var winWidth = $( window ).width();
$(".carousel-inner").css("font-size", winWidth/25.6);

function dropControl(){
    if(winWidth < 768){
        document.getElementById("dropdown_menu").style.position = "relative";
    } else{
        document.getElementById("dropdown_menu").style.position = "absolute";
    }

    if(document.getElementById("dropdown_menu").style.height == "82px"){
        document.getElementById("dropdown_menu").style.height = "0px";
    } else{
        document.getElementById("dropdown_menu").style.height = "82px";
    }
}

$(document).ready(function(){
  //resize font size when resolution change
  $(window).resize(function(){
    winWidth = $( window ).width();
    $(".carousel-inner").css("font-size", winWidth/25.6);
  })

  $("#addNew").click(function(e){
    $('#postModal').modal("show");
    e.preventDefault();
  });

    $('#searchForm').submit(function(e){
        search();
        e.preventDefault();
    });

    // $('#sqliForm').submit(function(e){
    //     search('#sqliForm');
    //     e.preventDefault();
    // });

    function search(formID){
        $.ajax({
            url: "http://localhost/CodeIgniter/pages/search",
            method: "GET",
            data: $(formID).serialize(),
            dataType: 'json',
            success: function (result) {
                for(var i=0; i < result.length; i++)
                    // console.log(result[i]);
                    $('#injRes').append('<div>' + result[i]["contents"] + '</div>')
            },
            error: function(jqXHR, textStatus, errorMessage) {
                console.log(errorMessage); // Optional
            }
        });
    }
});