// Some general UI pack related JS
// Extend JS String with repeat method
String.prototype.repeat = function(num) {
    return new Array(num + 1).join(this);
};

(function($) {

  // Add segments to a slider
  $.fn.addSliderSegments = function (amount) {
    return this.each(function () {
      var segmentGap = 100 / (amount - 1) + "%"
        , segment = "<div class='ui-slider-segment' style='margin-left: " + segmentGap + ";'></div>";
      $(this).prepend(segment.repeat(amount - 2));
    });
  };

  $(function() {
  
    // Todo list
    $(".todo li").click(function() {
        $(this).toggleClass("todo-done");
    });

    // Custom Selects
    $("select[name='huge']").selectpicker({style: 'btn-hg btn-primary', menuStyle: 'dropdown-inverse'});
    $("select[name='selectlist']").selectpicker({style: 'btn-primary', menuStyle: 'dropdown-inverse'});
    $("select[name='language']").selectpicker({style: 'btn-primary', menuStyle: 'dropdown-inverse'});
    $("select[name='info']").selectpicker({style: 'btn-info'});

    // Tooltips
    //$("[data-toggle=tooltip]").tooltip("show");

    // Tags Input
    //$(".tagsinput").tagsInput();

    // Placeholders for input/textarea
   // $("input, textarea").placeholder();

    // Make pagination demo work
    $(".pagination a").on('click', function() {
      $(this).parent().siblings("li").removeClass("active").end().addClass("active");
    });

    $(".btn-group a").on('click', function() {
      $(this).siblings().removeClass("active").end().addClass("active");
    });

    // Disable link clicks to prevent page scrolling
    $('a[href="#fakelink"]').on('click', function (e) {
      e.preventDefault();
    });

    // Switch
    //$("[data-toggle='switch']").wrap('<div class="switch" />').parent().bootstrapSwitch();
    
  });
  
})(jQuery);