// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeline', 'timelineEnd', 'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());

// Place any jQuery/helper plugins in here.
function alertBar($alertBar, isSuccess, msg) {
    if (isSuccess)
        $alertBar.removeClass('alert-warning').addClass('alert-success');
    else
        $alertBar.removeClass('alert-success').addClass('alert-warning');

    $alertBar.html(msg);

    $alertBar.fadeIn();
    setTimeout(function () {
        $alertBar.fadeOut();
    }, 5000);
}

function validateForm(form) {
    if (!form.checkValidity()) {
        $(form).addClass('was-validated');
        return false;
    }

    return true;
}

function redirectHomeAfterTimeout(seconds) {
    setTimeout(function () {
        window.location.replace('./index.html');
    }, seconds * 1000);
}

function executeAfterFetchingUsernameFromId(id, callback) {
    $alertBar = $('.alert');

    $.ajax({
        type: 'POST',
        url: '../../cgi-bin/513/1/GetUsernameFromId.cgi',
        data: {id: id},
        success: function (data, statusText) {
            if (data.status === 'success' && data.username !== '') {
                // Execute passed in callback function, which will somehow use the retrieved username
                callback(data.username);
            } else {
                alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve your username. You will be redirected back to the home page.');

                // Redirect user back to index page since we could not successfully retrieve their username
                redirectHomeAfterTimeout(3);
            }
        },
        error: function (xhr, statusText, errorText) {
            alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve your username. You will be redirected back to the home page.');

            // Redirect user back to index page since we could not successfully retrieve their username
            redirectHomeAfterTimeout(3);
        }
    });
}

function executeAfterFetchingPastPurchasesFromId(id, callback) {
    $alertBar = $(.alert);

    $.ajax({
        type: 'POST',
        url: '../../cgi-bin/GetPastPurchases.cgi',
        data: {id: id},
        success: function (data, statusText) {
            if (data.status === 'success') {
                // Execute passed in callback function, which will somehow use
                // the retrieved past purchases
                callback(data.purchases);
            } else {
                alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve your past purchases.')
            }
        },
        error: function (xhr, statusText, errorText) {
            alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve your past purchases.');
        }
    });
}
