(function($, Voer, document) {
    Voer.Materials = (function() {
        return {
            addFavorite : function (ele, params) {
                $.post('/ajax/add_favorite', params, function(data){
                    if (data.status) {
                        $('#voer-message-modal').find('.modal-title').html(data.message);
                        $('#voer-message-modal').modal('show');

                        $('#voer-message-modal').on('shown.bs.modal', function (e) {
                            window.setTimeout(function() {
                                $('#voer-message-modal').modal('hide');
                            }, 3000);
                        });

                        ele.html(data.favorite_count);
                    } else if (data.status === undefined) {
                        var currentUrl = window.location.pathname;
                        window.location.href = '/user/login/?next=' + currentUrl;
                    }
                });
            },
            materialRate: function(element, rate) {
                var parent_ele = $(element).parent();
                var mid = parent_ele.attr('data-material-id');
                var version = parent_ele.attr('data-material-version');

                var params = {};
                params.mid = mid;
                params.version = version;

                if (rate === undefined || rate == 0) {
                    params.rate = '';
                    params.type = 'delete';
                } else {
                    params.rate = rate;
                }

                $.ajax({
                    type: 'get',
                    url: '/ajax/user-rate',
                    data: params,
                    success: function(data) {
                        $('#material-rating').html(data);
                    }
                });
            }
        };
    })();

    Voer.Materials.run = function() {
        $(document).on('click', '.checkout-icon-favourite', function(){
            var btnSave = $(this);
            var mid = btnSave.attr('data-mid');
            var version = btnSave.attr('data-version');
            var csrfmiddlewaretoken = Voer.Helper.getCookie('csrftoken');

            Voer.Materials.addFavorite(btnSave, {mid: mid, version: version, csrfmiddlewaretoken: csrfmiddlewaretoken});
        });
    };
})(jQuery, window.Voer, window.document);
