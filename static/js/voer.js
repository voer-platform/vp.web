function ajax_browse(url, types, languages, categories){
    //Get value
    $.get(url , {types: types, languages: languages, categories: categories}, function( data ) {
        $("#materials" ).html( data );
    });
}
