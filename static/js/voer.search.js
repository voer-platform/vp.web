(function($, Voer, document) {
    Voer.Search = (function() {
        return {
            searchByCondition: function() {
                var params = Voer.Search.getSearchConditions();

                Voer.Helper.showLoadingState('.content-wrapper');
                $.get('/ajax/search-result', params, function(data){
                    Voer.Helper.removeLoadingState('.content-wrapper');
                    $('#materials').html(data);
                });
                return false;
            },
            getSearchConditions: function() {
                var params = {};
                params.keyword = $('#search-keyword').val();

                var search_type_array = new Array();
                $('.search-type .checkbox-custom.file_selected').each(function(){
                    search_type_array.push($(this).attr('data-value'));
                });
                params.search_type = search_type_array.join(',');

                var material_type_array = new Array();
                $('.material-type .checkbox-custom.file_selected').each(function(){
                    material_type_array.push($(this).attr('data-value'));
                });
                params.material_type = material_type_array.join(',');

                return params;
            }
        };
    })();

    Voer.Search.run = function() {
        $(document).on('click', '.smallbox-common .checkbox-item', function(){
            var multiable = false;
            if ($(this).parent().hasClass('multiable-select')){
                multiable = true;
            }

            if (multiable) {
                var datakey = $(this).parent().attr('data-key');
                var datavalue = $.trim($(this).find('.checkbox-custom').attr('data-value'));
                var chkbox = '.' + datakey + ' .checkbox-custom';
                if (datavalue == '') {
                    var $other_choices = $(chkbox + '[data-value!=""]');
                    $other_choices.removeClass('file_selected');
                    $other_choices.parent().parent().removeClass('file_selected');

                    var $all_choice = $(chkbox + '[data-value=""]');
                    $all_choice.addClass('file_selected');
                    $all_choice.parent().parent().addClass('file_selected');
                } else {
                    var $current_chk = $(chkbox + '[data-value="'+datavalue+'"]');
                    if ($current_chk.hasClass('file_selected')) {
                        $current_chk.removeClass('file_selected');
                        $current_chk.parent().parent().removeClass('file_selected');
                    } else {
                        $current_chk.addClass('file_selected');
                        $current_chk.parent().parent().addClass('file_selected');
                    }

                    var $all_choice = $(chkbox + '[data-value=""]');
                    if ($(chkbox + '[data-value!=""]').hasClass('file_selected')) {
                        $all_choice.removeClass('file_selected');
                        $all_choice.parent().parent().removeClass('file_selected');
                    } else {
                        $all_choice.addClass('file_selected');
                        $all_choice.parent().parent().addClass('file_selected');
                    }
                }
            } else {
                $(this).parent().find('.checkbox-custom').each(function(){
                    $(this).parent().parent().removeClass('file_selected');
                    $(this).removeClass('file_selected');
                });

                var $checkboxEle = $(this).find('.checkbox-custom');
                $checkboxEle.addClass('file_selected');
                $(this).children().addClass('file_selected');

                var search_type = $('.search-type .checkbox-custom.file_selected').attr('data-value');
                var $material_type = $('.material-type');
                if (search_type == 'm') {
                    $material_type.show();
                } else {
                    //reset option for material type
                    $material_type.find('.checkbox-custom').each(function(){
                        if ($.trim($(this).attr('data-value')) == '') {
                            $(this).addClass('file_selected');
                            $(this).children().addClass('file_selected');
                        } else {
                            $(this).removeClass('file_selected');
                            $(this).parent().parent().removeClass('file_selected');
                        }
                    });
                    $material_type.hide();
                }
            }

            Voer.Search.searchByCondition();
        });
    };
})(jQuery, window.Voer, window.document);