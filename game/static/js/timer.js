const zeroPad = (num, places) => String(num).padStart(places, '0')

$(function() {
    var build_end = document.getElementById("end_date").innerHTML;
    build_end = new Date(build_end);

    var interval = setInterval(function() {
        var time = new Date(build_end - Date.now());
        var seconds = time.getTime()/1000;
        var minutes = seconds/60;
        var hours = minutes/60;
        var days = hours/24;

        days = Math.floor(days);
        hours = Math.floor(hours%24);
        minutes = Math.floor(minutes%60);
        seconds = Math.floor(seconds%60);

        var output = zeroPad(hours, 2) + ":" + zeroPad(minutes, 2) + ":" + zeroPad(seconds, 2);

        if(days > 0) 
            output = "Dni: " + days + " | " + output;

        document.getElementById("time_last").innerHTML = output;

        if (Date.now() >= build_end)
            clearInterval(interval);
    }, 1000);
});