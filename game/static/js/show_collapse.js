$(function() {
    var show = true;
    var ids = [
        'production_drewno',
        'production_kamień',
        'production_jedzenie',
        'build'
    ];
    
    setTimeout(toggle_collapse, 1000)
    setTimeout(toggle_collapse, 5000)

    function toggle_collapse() {
        show = !show;

        for(let id of ids) {
            var for_id = id;
            id = 'collapse_' + id;
            var collapse = document.getElementById(id);
            
            if(collapse) {
               collapse = collapse.classList;

                if(show == false) {
                    $('#' + id).collapse('toggle');
                    collapse.add("show")
                } else {
                    // Don't hide 'collapse_build'
                    if(ids.indexOf(for_id) < 3) {
                        $('#' + id).collapse('toggle');
                        collapse.remove("show")
                    }
                }
            }
        }
    }
});