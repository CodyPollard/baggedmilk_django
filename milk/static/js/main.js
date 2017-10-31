function getSystems() {
    var url, systemOptions;
    url = 'JSON_FINAL.json';

    $.getJSON(json_file, function(data) {
    // Populate the systems datalist
        $(data.allSystems).each(function() {
            systemOptions = "<option value=\"" + this.system + "\">" + this.security + "</option>";
            $('#json-datalist').append(systemOptions);
        });
    });
}