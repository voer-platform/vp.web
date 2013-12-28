var Voer = {};

function ajax_browse(url, types, languages, categories){
    //Get value
    $("#materials").html('<div class="bg-loading"><img src="/static/images/loading.gif" height="31" width="31" alt="loading..." /></div>');
    $.get(url , {types: types, languages: languages, categories: categories}, function( data ) {
        $("#materials" ).html( data );
    });
}

(function($, Voer, document) {
    Voer.Helper = (function(){
      return {
        login: function (){
          var formLogin = $('#login-form');
          var url = formLogin.attr('action');
          var messageObj = formLogin.find('.alert-modal-login');
          messageObj.addClass('hidden');

          $.post(url, formLogin.serialize(), function(data){
            if (data.status == 1) {
              window.location.href = "/";
            } else {
              messageObj.children().html(data.message);
              messageObj.fadeIn("fast", function() {
                $(this).removeClass('hidden');
              });
            }
          });

          return false;
        },
        showPassword: function(checkboxEle, passwordEle) {
          if ($(checkboxEle).is(':checked')) {
            $(passwordEle).attr('type', 'text');
          } else {
            $(passwordEle).attr('type', 'password');
          }
        }
      };
    })();
})(jQuery, window.Voer, window.document);
