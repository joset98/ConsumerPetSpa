$(document).ready(function(){

// Verificar si existe una conversacion en curso
if ($.cookie("chatToken") != null) 
{
    //se llama a funcion para obtener conversacion si existe
    obtenerConversacion($.cookie("chatToken"));
}


// Toggle para abrir y cerrar box-chat
$(".title-chat").click(function() {
      $(".box-chat").toggle("fast");
	});
// boton externo para abrir y cerrar box-chat
$(".chatnowbutton").click(function() {
      $(".box-chat").toggle("fast");
      return false;
  });

});


// Funcionalidad del chat
$(function() {
    'use strict';
    $('#chat-form').on('submit', function() {
      if ($('.input-mensaje').val() != '') {
        var post_url = $("#chat-form").data("post-url");
        var formData = new FormData(this);
        var mensajee = formData.get('mensaje');
        var tiempo = new Date();
        var hora = tiempo.getHours();
        var minuto = tiempo.getMinutes();
        hora = hora+':'+minuto;
        $.ajax({
            url : post_url,
            type: "POST",
            data : formData,
            processData: false,
            contentType: false,
            success:function(response){
            	// Agregar mensaje del cliente al chat box
            	$('.input-mensaje').val('');

              if (response.content.estado == 'enviado') {
                $('.body-chat').append('<div class="mensaje-c"><p class="cl">'+mensajee+'</p></div>'+'<span class="info-c">'+$.cookie("chatUser")+' - '+hora+'</span>');
                $(".body-chat").scrollTop(100000000000000);
                tiempo = new Date();
                hora = tiempo.getHours();
                minuto = tiempo.getMinutes();
                hora = hora+':'+minuto;
                // Agregar mensaje del bot al chat box
                var mensaje = response.content.mensaje;
                setTimeout(function(){
                    document.getElementById('tono').play();
                    $('.body-chat').append('<div class="mensaje-s"><p class="se">'+mensaje+'</p></div><span class="info-s">Bot - '+hora+'</span>');
                    $(".body-chat").scrollTop(100000000000000);
                }, 1500);
              }

              if (response.content.error == 'token no valido') {
                    $.removeCookie("chatToken", { path: '/' });
                    $.removeCookie("chatUser","null",{ path: '/' });
                    $('.button-create-chat').attr("disabled", false);
                    $('.ocultar-chat').hide();
                    $('.create-chat').show();
              }

            },
        });
        return false;
      } else
        return false;
    });
});

  // crear chat
  $(function() {
      'use strict';
      $('#create-chat-form').on('submit', function() {
          $('.button-create-chat').attr("disabled", true);
          var post_url = $("#create-chat-form").data("post-url");
          var formData = new FormData(this);
          $('.create-chat-nombre').val('');
          $('.create-chat-correo').val('');
          $.ajax({
              url : post_url,
              type: "POST",
              data : formData,
              processData: false,
              contentType: false,
              success:function(response){
                if (response.content.estado == 'creado') {
                    $.cookie("chatToken",response.content.token,{ path: '/' });
                    $("input[name='token']").val(response.content.token);
                    $.cookie("chatUser",formData.get('nombre'),{ path: '/' });
                    $('.ocultar-chat').show();
                    $('.create-chat').hide();
                }
              },
          });
          return false;
      });
  });


function obtenerConversacion(token){
  var formData = new FormData();
  var vtoken = $.cookie("csrftoken");
  var post_url = $("#chat-form").data("post-get-url");
  formData.append("token", token);
  $.ajax({
      headers: { "X-CSRFToken": vtoken },
      url : post_url,
      type: "POST",
      data : formData,
      processData: false,
      contentType: false,
      success:function(response){
        if (response.content.estado == 'recibido') {
            $("input[name='token']").val($.cookie("chatToken"));
            $('.ocultar-chat').show();
            $('.create-chat').hide();
          // Rellenar mensajes
          for(var i = 0; i < response.content.mensajes.length; i++) {
            var aux =response.content.mensajes[i];
            var fechaString = aux.fecha;
            var fechaActual = new Date(parseInt(fechaString ));
            if(aux.tipo == "c"){
               $('.body-chat').append('<div class="mensaje-c"><p class="cl">'+aux.mensaje+'</p></div><span class="info-c">'+$.cookie("chatUser")+'</span>');
            }

            if(aux.tipo == "s"){
               $('.body-chat').append('<div class="mensaje-s"><p class="se">'+aux.mensaje+'</p></div><span class="info-s">Bot</span>');
            }
          }
          $(".box-chat").toggle("fast");
          $(".body-chat").scrollTop(100000000000000);
        }
        if (response.content.error == 'token no valido') {
            $.removeCookie("chatToken", { path: '/' });
            $.removeCookie("chatUser","null",{ path: '/' });
            $('.button-create-chat').attr("disabled", false);
            $('.ocultar-chat').hide();
            $('.create-chat').show();
        }
      },
  });
};
