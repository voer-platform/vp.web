/**
 * Created by huyvq on 28/12/2013.
 */
$(document).ready(function(){
    $("#collection-outline").jstree({
        "plugins" : [
            "themes","json_data","ui","crrm","cookies","dnd","search","types","hotkeys", "contextmenu"
        ],
        "json_data" : {
            "data" : $('#voer-outline-text').val() ? jQuery.parseJSON($('#voer-outline-text').val()) : []
        },
        "types" : {
            // I set both options to -2, as I do not need depth and children count checking
            // Those two checks may slow jstree a lot, so use only when needed
            "max_depth" : -2,
            "max_children" : -2,
            "valid_children" : [ "root" ],
            "types": {
                "module" : {
                    "valid_children" : "none"
                },
                "bundle" : {
                    "valid_children" : [ "module", "bundle" ]
                },
                "root":{
                    // can have files and folders inside, but NOT other `drive` nodes
                    "valid_children" : [ "module", "bundle" ],
                    "icon" : {
                        "image" : "/static/images/kdm_home.png"
                    },
                    // those prevent the functions with the same name to be used on `drive` nodes
                    // internally the `before` event is used
                    "start_drag" : false,
                    "move_node" : false,
                    "delete_node" : false,
                    "remove" : false
                }
            }
        }
    })
    .bind("create.jstree", function (e, data) {
        var jsonData = $("#collection-outline").jstree('get_json', -1);
        var jsonStr =  JSON.stringify(jsonData);
        $('#voer-outline-text').val(jsonStr);
    })
    .bind("remove.jstree", function (e, data) {
        var jsonData = $("#collection-outline").jstree('get_json', -1);
        var jsonStr =  JSON.stringify(jsonData);
        $('#voer-outline-text').val(jsonStr);
    })
    .bind("rename.jstree", function (e, data) {
        var jsonData = $("#collection-outline").jstree('get_json', -1);
        var jsonStr =  JSON.stringify(jsonData);
        $('#voer-outline-text').val(jsonStr);
    })
    .bind("move_node.jstree", function (e, data) {
        var jsonData = $("#collection-outline").jstree('get_json', -1);
        var jsonStr =  JSON.stringify(jsonData);
        $('#voer-outline-text').val(jsonStr);
    });

    $("div#outline-actions input").click(function () {
        switch(this.id) {
            case "add_default":
                $("#voer_module_search_result input[type=checkbox]:checked").map(function(){
                    if (!$(this).attr('disabled')) {
                        var id = $(this).val();
                        var title = $(this).parent().find('.voer-content-title').text().trim();
                        var parentNode = -1;
                        if ($("#collection-outline").jstree("get_selected")){
                            if ($("#collection-outline").jstree("get_selected").length > 1){
                                parentNode = $('ul>li#root-outline');
                            }else{
                                var selected = $("#collection-outline").jstree("get_selected");
                                if (selected.attr("rel") == "bundle" || selected.attr("rel") == "root"){
                                    parentNode = null;
                                }else{
                                    parentNode = $('ul>li#root-outline');
                                }
                            }
                        }
                        $("#collection-outline").jstree("create", parentNode, "last", { "data": title, "attr" : { "id": id, "rel" : "module" } });
                        $(this).attr('disabled', 'disabled');
                        $("#collection-outline").find('input.jstree-rename-input').blur();
                    }
                });
                break;
            case "search":
                $("#collection-outline").jstree("search", document.getElementById("text").value);
                break;
            case "info":
                var jsonData = $("#collection-outline").jstree('get_json', -1);
                var jsonStr =  JSON.stringify(jsonData);
                console.log(jsonStr);
                break;
            case 'remove':
                $("#collection-outline").jstree('get_selected').each(function(){
                   var material_id = $(this).attr('id');
                   $('#voer_module_search_result input[value="'+material_id+'"]').removeAttr('disabled').removeAttr('checked');
                });
                $("#collection-outline").jstree(this.id);
                break;
            default:
                $("#collection-outline").jstree(this.id);
                break;
        }

        var jsonData = $("#collection-outline").jstree('get_json', -1);
        var jsonStr =  JSON.stringify(jsonData);
        $('#voer-outline-text').val(jsonStr);

        return false;
    });

    jQuery('.voer-module-search-text').keypress(function(e){
        if (e.which == 13){
            var keyword = jQuery('.voer-module-search-text').val();
            searchModuleByKeyword(keyword);
            return false;
        }
    });

//    $('.voer-module-search-btn', context).click(function () {
//        var keyword = jQuery('.voer-module-search-text').val();
//        searchModuleByKeyword(keyword);
//        return false;
//    });

    $('#btn_add_sections').click(function () {
        var voer_sub_sessions = $('#voer_sub_sessions').val();

        if (!voer_sub_sessions) {
            alert('Please enter something');
            return false;
        }
        var session_array = voer_sub_sessions.split("\n");

        $.each(session_array, function(index){
            if ($.trim(session_array[index])) {
                var parentNode = -1;
                if ($("#collection-outline").jstree("get_selected")){
                    if ($("#collection-outline").jstree("get_selected").length > 1){
                        parentNode = $('ul>li#root-outline');
                    }else{
                        var selected = $("#collection-outline").jstree("get_selected");
                        if (selected.attr("rel") == "bundle" || selected.attr("rel") == "root"){
                            parentNode = null;
                        }else{
                            parentNode = $('ul>li#root-outline');
                        }
                    }
                }
                $("#collection-outline").jstree("create", parentNode, "last", { "data": session_array[index], "attr" : { "rel" : "bundle" } });
            }
        });

        $('#voer_sub_sessions').val('');
        $('.modal_close').trigger('click');
        $("#collection-outline").find('input.jstree-rename-input').blur();
    });
});

function searchModuleByKeyword(keyword, page) {
    if (page === undefined) {
        page = 1;
    }

    var collection_selected = jQuery('#voer-outline-text').val();

    if (jQuery('#voer_module_search_result').length == 0) {
        jQuery('<div id="voer_module_search_result"></div>').appendTo('#voer-outline-wrapper');
    }

    //showLoadingState('#edit-field-voer-authors');

    jQuery.post('/ajax/s/m', {keyword: keyword, page: page, collection_selected: collection_selected}, function (data) {
        // removeLoadingState('#edit-field-voer-authors');
        jQuery('#voer_module_search_result').html(data);
    })
}

function loadModuleSearchPage(ele) {
    var keyword = jQuery(ele).attr('keyword');
    var page = jQuery(ele).attr('page');
    searchModuleByKeyword(keyword, page);
    return false;
}