function collapse_toggle(id) {
    var collapse = document.getElementById(id);

    if(collapse) {
        collapse = collapse.classList;

        if(collapse.contains('show')) {
            $('#' + id).collapse('toggle');
            collapse.remove("show");
        } else {
            $('#' + id).collapse('toggle');
            collapse.add("show");
        }
    }
}