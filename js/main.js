(function ($) {

    buildFooter();

})(jQuery);

function buildFooter() {
    $('body').append(
        $('<footer>', {class: 'navbar fixed-bottom navbar-dark bg-dark'}).append(
            $('<div>', {class: 'container'}).append(
                $('<a>', {href: '#', class: 'navbar-brand'}),
                $('<ul>', {class: 'navbar-nav mr-auto'}).append(
                    $('<li>', {class: 'nav-item'}).append(
                        $('<a>', {href: 'https://github.com/KeltonKarboviak/CSci513_1', class: 'nav-link'}).append(
                            $('<span>', {class: 'oi oi-terminal oi-label'}),
                            document.createTextNode(' View Source')
                        )
                    )
                )
            )
        )
    );
}
