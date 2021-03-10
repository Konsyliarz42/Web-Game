function collapse_toggle(id) {
    var collapse = document.getElementById(id);
    var collapse_group = $('.collapse-group');
    var parent = collapse.closest('div');

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

    if(collapse_group) {
        collapse_group = collapse_group.children();
        
        for(var index = 0; index < collapse_group.length; index++) {
            collapse = collapse_group[index];

            if(id != collapse['id'] && collapse.classList.contains('show') && parent.classList.contains('card-body')) {
                $('#' + collapse['id']).collapse('toggle');
                collapse.classList.remove("show");
            }
        }
    }
}