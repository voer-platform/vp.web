(function($, Voer, document) {
    Voer.Materials = (function() {
        return {
            addFavorite : function (ele, params) {
                var type = 'insert';
                var is_multiple = false;

                if (Voer.Helper.hasAttr(ele, 'data-added-favorite')) {
                    type = 'delete';
                }
                params.type = type;

                if (params.is_multiple) {
                    is_multiple = true;
                }

                $.post('/ajax/add_favorite', params, function(data){
                    if (data.status) {
                        if (is_multiple) {
                            $('.icon-favorite').each(function(){
                                Voer.Materials._updateFavoriteInfo($(this), data);
                            });
                        } else {
                            Voer.Materials._updateFavoriteInfo(ele, data);
                        }

                        Voer.Helper.showMessagePopup(data.message);
                    } else if (data.status === undefined) {
                        var currentUrl = window.location.pathname;
                        window.location.href = '/user/login/?next=' + currentUrl;
                    }
                });
            },
            _updateFavoriteInfo: function(ele, data) {
                if (data.is_favorited) {
                    $(ele).addClass('active').attr('data-added-favorite', 'True');
                } else {
                    $(ele).removeClass('active').removeAttr('data-added-favorite');
                }
                ele.next('.stats-count').html(data.favorite_count);
            },
            materialRate: function(element, rate) {
                var parent_ele = $(element).parent();
                var mid = parent_ele.attr('data-material-id');
                var version = parent_ele.attr('data-material-version');

                if (rate === undefined) {
                    rate = 0;
                }

                var params = {};

                params.mid = mid;
                params.version = version;

                if (rate === undefined || rate == 0) {
                    params.rate = rate;
                    params.type = 'delete';
                } else {
                    params.rate = rate;
                }

                $.ajax({
                    type: 'get',
                    url: '/ajax/user-rate',
                    data: params,
                    success: function(data) {
                        if (data.success === false) {
                            var rating_material = mid + '-' + version + '-' + rate;
                            Voer.Helper.createCookie('rating_material', rating_material);

                            var currentUrl = window.location.pathname;
                            window.location.href = '/user/login/?next=' + currentUrl;
                        } else {
                            $('#material-rating').html(data);
                        }
                    }
                });
            }
        };
    })();

    Voer.Materials.run = function() {
        $(document).on('click', '.icon-favorite', function(){
            var btnSave = $(this);
            var btnSaveParent = btnSave.parent();
            var mid = btnSave.attr('data-material-id');
            var version = btnSave.attr('data-material-version');
            var csrfmiddlewaretoken = Voer.Helper.getCookie('csrftoken');
            var is_multiple = Voer.Helper.hasAttr(btnSave, 'data-is-multiple');

            if (Voer.Helper.hasAttr(btnSaveParent, 'disabled')) {
                return false;
            }

            btnSaveParent.attr('disabled', 'disabled');
            setTimeout(function(){
                btnSaveParent.removeAttr('disabled');
            }, 3000);

            Voer.Materials.addFavorite(btnSave, {mid: mid, version: version, csrfmiddlewaretoken: csrfmiddlewaretoken, is_multiple: is_multiple});
        });
    };
})(jQuery, window.Voer, window.document);
