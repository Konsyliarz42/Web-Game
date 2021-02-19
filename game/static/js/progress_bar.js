$(function() {
    var start_date = document.getElementById("start_date").innerHTML;
    var end_date = document.getElementById("end_date").innerHTML;

    start_date = new Date(start_date).getTime();
    end_date = new Date(end_date).getTime() - start_date;
        
    var interval = setInterval(function() {
        var now_date = Date.now() - start_date;
        var percent = (now_date/end_date)*100;
            
        $('.progress-bar')
        .css("width", percent + "%")
        .attr("aria-valuenow", now_date)
        .text(percent.toFixed(1) + "%")
            
        if (now_date >= end_date)
        {
            clearInterval(interval);
            window.location.reload(true);
        }
    }, 1000);
});