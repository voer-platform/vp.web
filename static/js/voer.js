var Voer = {};

function ajax_browse_page(url){
    var target = '#materials';
    Voer.Helper.showLoadingState(target);
    $.get(url, function(data){
        $('#materials').html(data);
        Voer.Helper.removeLoadingState(target);
    });
}

function ajaxGetMaterialByCondition() {
    var author_id = $('#filter-author-id').val();
    var sort = $('#filter-sort').val();
    var page = 1;

    //Get values
    var listItems = [];
    $('#main_list').find('.checkbox-custom.file_selected').each(function(){
        listItems.push($(this).attr('data-key'));
    });
    var numberItem = listItems.length;
    var html='';
    var types = [];
    var langs = [];
    var categories = [];
    for(var i = 0; i < numberItem; i++){
        if(listItems[i].substr(0, 6) == 'types-'){
            types.push(listItems[i].substr(6));
        }else if(listItems[i].substr(0,6) == 'langs-'){
            langs.push(listItems[i].substr(6));
        }else if(listItems[i].substr(0,11) == 'categories-'){
            categories.push(listItems[i].substr(11));
        }
    }

    if(numberItem > 0){
        $('#selection-actions').removeClass('displaynone');
        $('.selected_count').html(numberItem);
    }else{
        $('#selection-actions').addClass('displaynone');
    }

    $("#materials").html('<div class="bg-loading"><img src="/static/images/loading.gif" height="31" width="31" alt="loading..." /></div>');
    $.get('/ajax/browse' , {author: author_id, types: types.join(","), languages: langs.join(","), categories: categories.join(","), sort: sort}, function( data ) {
        $("#materials" ).html(data);
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
              window.location.href = "/user/dashboard";
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
        },
        getCookie: function(name){
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?

                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },
        ajaxCatcher: function(){
          $('.ajax-ev[data-ajax-trigger="load"]').each(function(){
            var $this = $(this);
            var url = $this.attr('data-ajax-url');
            var target = $this.attr('data-ajax-target') || '#' + $(this).attr('id');
            _run(url, target);
          });
          $(document).on('click','.ajax-ev[data-ajax-trigger!="load"]', function(){
            var $this = $(this);
            var url = $this.attr('data-ajax-url');
            var target = $this.attr('data-ajax-target') || '#' + $(this).attr('id');
            _run(url, target);
          });

          function _run(url, target) {
            var $target = $(target);
            Voer.Helper.showLoadingState(target);
            $.ajax(url,{
              success: function(r){
                Voer.Helper.removeLoadingState(target);
                $target.html(r);
              },
              error: function() {
                Voer.Helper.removeLoadingState(target);
              }
            });
          }
        },
        showLoadingState: function(element) {
          Voer.Helper.removeLoadingState(element);

          if (element === undefined) {
            element = 'document';
            var coordinate = {top:0, left: 0};
            var loadingWidth = $(window).width() - 2;
            var loadingHeight = $(window).height() - 2;

          } else {
            var coordinate = $(element).offset();
            var loadingWidth = $(element).width() - 2;
            var loadingHeight = $(element).height() - 2;
          }

          if (loadingWidth == -2) {
            loadingWidth = 350;
          }

          if (loadingHeight == -2) {
            loadingHeight = 32;
          }

          var div = $(document.createElement('div'));
          var elementId = element.substring(1);

          div.attr('id', elementId + '-loading');
          div.attr('class', 'ajax-loading');
          if (coordinate) {
            div.css({
              width: loadingWidth,
              height: loadingHeight,
              position: element == 'document' ? 'fixed' : 'absolute',
              zIndex: element == 'document' ? '2' : '40',
              top: coordinate.top + 1,
              left: element == 'document' ? (coordinate.left + 1) : (coordinate.left + 1 + parseInt($(element).css('padding-left')))
            });
          }

          var loadingMargin = Math.round((loadingHeight / 2) - 16);
          var content = '<div style="text-align:center;margin-top:' + loadingMargin + 'px"><img src="/static/images/ajax-loader.gif" /></div>';

          div.html(content);
          div.appendTo('body');
        },
        removeLoadingState: function(element) {
          if (element === undefined) {
            element = '#document';
          } else {
            element = '#' + element.substring(1);
          }

          $(element + '-loading').remove();
        },
        rating: function (element) {
            var isDisabled = false;

            if (Voer.Helper.hasAttr(element, 'data-rated-flag')) {
                isDisabled = true;
            }

            $(element).jRating({
                bigStarsPath: '/static/css/jquery/jRating/icons/stars.png',
                smallStarsPath: '/static/css/jquery/jRating/icons/small.png',
                rateMax: 5,
                isDisabled: isDisabled,
                sendRequest: false,
                step: true,
                onClick: function(obj, rate) {
                    Voer.Materials.materialRate(obj, rate);
                }
            });
        },
        hasAttr: function(element, field_name) {
            var has_attr = false;
            var attr = $(element).attr(field_name);

            // For some browsers, `attr` is undefined; for others, `attr` is false.  Check for both.
            if (typeof attr !== 'undefined' && attr !== false) {
                has_attr = true;
            }

            return has_attr;
        },
        createCookie: function(name, value, days) {
          var expires = "";

          if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toGMTString();
          }

          document.cookie = name+"="+value+expires+"; path=/";
        },
        readCookie: function(name) {
          var nameEQ = name + "=";
          var ca = document.cookie.split(';');

          for (var i=0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
          }

          return null;
        },
        eraseCookie: function(name) {
          this.createCookie(name, "", -1);
        },
        showMessagePopup: function(message, params) {
          var setting_default = {
            ele: 'body', // which element to append to
            type: 'success', // (null, 'info', 'danger', 'success')
            offset: {from: 'top', amount: 70}, // 'top', or 'bottom'
            align: 'center', // ('left', 'right', or 'center')
            width: 'auto', // (integer, or 'auto')
            delay: 3000 // Time while the message will be displayed. It's not equivalent to the *demo* timeOut!
          };

          var settings = $.extend({}, setting_default, params);

          $('.bootstrap-growl').remove();
          $.bootstrapGrowl(message, settings);
        }
      };
    })();
})(jQuery, window.Voer, window.document);

(jQuery)(function($){
    Voer.Helper.ajaxCatcher();

    $(document).on('click', '.fiterbutton .gridview', function(){
        $('.hfitems').toggleClass('gridview');
        $('.gridview').toggleClass('active');
        $('.listview').toggleClass('active');
    });

     $(document).on('click', '.fiterbutton .listview', function(){
        $('.hfitems').toggleClass('gridview');
        $('.gridview').toggleClass('active');
        $('.listview').toggleClass('active');
    });
});
