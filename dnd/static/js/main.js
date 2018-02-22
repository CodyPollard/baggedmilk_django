function timerTest() {
    var start = new Date(selected_date);
    var d = 0;

    setInterval(function() {
        var timeSince = Math.round((new Date - start) / 1000, 0)
        // Do math and shit
        d = Math.floor(timeSince / 86400);
        var h = Math.floor(timeSince % 86400 / 3600);
        var m = Math.floor(timeSince % 3600 / 60);
        var s = Math.floor(timeSince % 60);
        // Format time for display
        $('.timer-clock').text(d + "d, " + h + "h, " + m + "m, " + s + "s")
    }, 1000);

}

function drawPucks(d) {
    console.log("Start of For Loop");
    console.log(d)
    for (i = 0; i < d; i++) {
        document.getElementById("pucks").appendChild(puckImg);
    }
    console.log("End of For Loop");
}

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