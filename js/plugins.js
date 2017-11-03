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

function redirectToDashboardAfterTimeout(dashboard_link, seconds) {
    setTimeout(function () {
        window.location.replace(dashboard_link);
    }, seconds * 1000);
}

function redirectHomeAfterTimeout(seconds) {
    setTimeout(function () {
        window.location.replace('./index.html');
    }, seconds * 1000);
}

function setDashboardLinkInNavbar(isAdmin, userId) {
    var href = isAdmin
        ? './admindash.html'
        : './userdash.html?id=' + userId;

    $('#a_dashboard').attr('href', href);
}

function insertUsernameInPlaceholders(username) {
    // This will set the html of every span that expects the user's username
    $('span.cust-name').html(username);
}

function purchasesToTable(purchases, params) {
    // Clear out the table body for upcoming results
    $('table#table_account > tbody').empty('');

    purchases.forEach(function (p) {
        $('<tr>').append(
            $('<td>').append(
                $('<a>').attr('href', './game-details.html?asin=' + p.asin + '&' + $.param(params)).html(p.title)
            ),
            $('<td>').html(p.quantity),
            $('<td>').attr('class', 'text-right').html('$ ' + p.total)
        ).appendTo('table#table_account > tbody');
    });
}

function gameDetailToCard(title, price, devs, params) {
    return $('<ul>', {class: 'list-group'}).append(
        $('<li>', {class: 'list-group-item'}).text('Title: ' + title),
        $('<li>', {class: 'list-group-item'}).text('Price: $' + price),
        devs.map(function (d) {
            return $('<li>', {class: 'list-group-item'}).append(
                document.createTextNode('Dev Name: '),
                $('<a>', {
                    // We append the passed in url params to the end of the href
                    // since it contains the current values of the user's id
                    // & whether it's an admin or not
                    href: './dev-details.html?dev_id=' + d.id + '&' + $.param(params)
                }).text(d.name)
            );
        })
    )
}

function devDetailToCard(name, games, params) {
    return $('<ul>', {class: 'list-group'}).append(
        $('<li>', {class: 'list-group-item'}).text('Name: ' + name),
        games.map(function (g) {
            return $('<li>', {class: 'list-group-item'}).append(
                document.createTextNode('Game Title: '),
                $('<a>', {
                    // We append the passed in url params to the end of the href
                    // since it contains the current values of the user's id
                    // & whether it's an admin or not
                    href: './game-details.html?asin=' + g.asin + '&' + $.param(params)
                }).text(g.title)
            );
        })
    )
}

function executeAfterFetchingUsernameFromId(id, callback) {
    $alertBar = $('.alert');

    $.ajax({
        type: 'POST',
        url: '../../cgi-bin/513/1/GetUsernameFromId.cgi',
        data: {id: id},
        success: function (data, statusText) {
            if (data.status === 'success' && data.username !== '') {
                // Execute passed in callback function, which will somehow use
                // the retrieved username
                callback(data.username);
            } else {
                alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve your username. You will be redirected back to the home page.');

                // Redirect user back to index page since we could not
                // successfully retrieve their username
                redirectHomeAfterTimeout(3);
            }
        },
        error: function (xhr, statusText, errorText) {
            alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve your username. You will be redirected back to the home page.');

            // Redirect user back to index page since we could not successfully
            // retrieve their username
            redirectHomeAfterTimeout(3);
        }
    });
}

function executeAfterFetchingPastPurchasesFromId(id, callback) {
    $alertBar = $('.alert');

    $.ajax({
        type: 'POST',
        url: '../../cgi-bin/513/1/GetPastPurchases.cgi',
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

/**
 * This function will create an AJAX call to the back-end implementation for
 * fetching details for 1 or all games.
 *
 * @param asin string The unique ASIN for the game to be fetched. If a true
 *                    value is passed in for fetchAll, this will be ignored.
 * @param fetchAll int A boolean value represented as an int (0 for false, true
 *                     for all other values) for whether the details for all
 *                     games in the database should be fetched or not.
 * @param callback function This is a callback function to be called once the
 *                          results have been successfully fetched. The callback
 *                          will be passed in the resulting array of game
 *                          details. It will always be an array regardless of
 *                          the value of fetchAll.
 */
function executeAfterFetchingGameDetails(asin, fetchAll, callback) {
    $alertBar = $('.alert');

    $.ajax({
        type: 'GET',
        url: '../../cgi-bin/513/1/GetGameDetails.cgi',
        data: {asin: asin, fetchAll: fetchAll},
        success: function (data, statusText) {
            if (data.status === 'success' && data.details.length > 0) {
                callback(data.details);
            } else {
                alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve this game\'s details.');
            }
        },
        error: function (xhr, statusText, errorText) {
            alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve this game\'s details.');
        }
    });
}

function executeAfterFetchingDevDetails(devId, callback) {
    $alertBar = $('.alert');

    $.ajax({
        type: 'GET',
        url: '../../cgi-bin/513/1/GetDevDetails.cgi',
        data: {id: devId},
        success: function (data, statusText) {
            if (data.status === 'success' && ! $.isEmptyObject(data.details)) {
                callback(data.details);
            } else {
                alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve this developer\'s details.');
            }
        },
        error: function (xhr, statusText, errorText) {
            alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve this developer\'s details.');
        }
    });
}

function executeAfterFetchingAllDevelopers(callback) {
    $alertBar = $('.alert');

    $.ajax({
        type: 'GET',
        url: '../../cgi-bin/513/1/GetAllDevNames.cgi',
        success: function (data, statusText) {
            if (data.status === 'success') {
                callback(data.devs);
            } else {
                alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve all developers.');
            }
        },
        error: function (xhr, statusText, errorText) {
            alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve all developers.');
        }
    });
}

function executeAfterFetchingAllGames(callback) {
    $alertBar = $('.alert');

    $.ajax({
        type: 'GET',
        url: '../../cgi-bin/513/1/GetAllGameTitles.cgi',
        success: function (data, statusText) {
            if (data.status === 'success' && data.games.length > 0) {
                callback(data.games);
            } else {
                alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve all games.');
            }
        },
        error: function (xhr, statusText, errorText) {
            alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve all games.');
        }
    });
}

function executeAfterFetchingAllCustomers(callback) {
    $alertBar = $('.alert');

    $.ajax({
        type: 'GET',
        url: '../../cgi-bin/513/1/GetAllCustNames.cgi',
        success: function (data, statusText) {
            if (data.status === 'success' && data.customers.length > 0) {
                callback(data.customers);
            } else {
                alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve all customers.');
            }
        },
        error: function (xhr, statusText, errorText) {
            alertBar($alertBar, false, '<strong>Warning!</strong> An error occurred trying to retrieve all customers.');
        }
    });
}
