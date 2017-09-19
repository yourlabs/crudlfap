window.crudlfap = {}

window.crudlfap.setBase = function(url, base) {
    if (url.search(/\?/) < 0) {
        url += '?'
    }

    if (url.search('&base=') > 0) {
        url = url.replace(/base=[^&]*/, 'base=' + base)
    } else {
        url += '&base=' + base
    }
    return url
}

window.crudlfap.unsetBase = function(url) {
    return url.replace(/base=[^&]*&/, '')
}

/* Load a URL in ajax and update #ajax-replace and friends.
 */
window.crudlfap.ajaxLoad = function(url) {
    ajaxUrl = window.crudlfap.setBase(url, 'ajax');
    callback = function(data) {
        var newTitle = $(data).filter('#html-title').html()
        $('title').html(newTitle);
        window.history.pushState(null, newTitle, window.crudlfap.unsetBase(url));
    }
    $('#ajax-replace').load(ajaxUrl, callback)
}

/* Intercept clicks to ajaxify requests.
 *
 * Do nothing if href starts with '#', open link in a modal if
 * data-target=model.
 */
$('body').on('click', 'a', function(e) {
    if ($(this).attr('href').startsWith('#')) {
        return;
    }

    var $target, callback
    var url = $(this).attr('href');

    e.preventDefault();

    if ($(this).attr('data-target') == 'modal') {
        $target = $('#modal .modal-dialog');
        callback = function() {
            $('#modal').modal()
            $('#modal').find(':input:first').focus()
        }
        url = window.crudlfap.setBase(url, 'modal');
        $target.load(url, callback);
    } else {
        window.crudlfap.ajaxLoad(url);
    }
});

window.onpopstate = function(event) {
  window.crudlfap.ajaxLoad(document.location.href);
};

$('body').on('shown.bs.modal', function (e) {
    $(e.target).find(':input:first').focus()
;
});

/* Intercept submits to ajaxify requests.
 */
$('body').on('submit', 'form', function(e) {
    e.preventDefault();

    var form = $(this);

    // Get form data before disabling fields
    var formData = new FormData(form[0])

    // Disable inputs to prevent double posting ... 2017 FTW <3
    form.find(':input').attr('disabled', 'disabled');

    // Show form loading div
    form.find('.form-loading').show();

    var modal = $(this).parents().find('.modal-dialog')
    var target = modal.length ? 'modal' : 'ajax'

    $.ajax({
        url: window.crudlfap.setBase(form.attr('action'), target),
        type: 'POST',
        data: formData,

        // Tell jQuery not to process data or worry about content-type
        // You *must* include these options!
        cache: false,
        contentType: false,
        processData: false,

        complete: function(jqXHR) {
            var $data = $(jqXHR.responseText);
            var $form = $data.filter('form');
            if (!$form.length) $form = $data.find('form');

            if ($form.length && $form.hasClass('form-invalid')) {
                modal.html($data);
            } else {
                var newTitle = $data.filter('title').html()
                $('title').html(newTitle);

                var $ajaxReplace = $data.filter('#ajax-replace')
                window.history.pushState(
                    null,
                    newTitle,
                    window.crudlfap.unsetBase(
                        $ajaxReplace.attr('data-full-path')
                    )
                );
                $('#ajax-replace').html($ajaxReplace.html());
                modal.parent().modal('hide');
            }
        },
        // Custom XMLHttpRequest
        xhr: function() {
            var myXhr = $.ajaxSettings.xhr();
            if (myXhr.upload) {
                // Disable form inputs during upload
                form.find(':input').attr('disabled', 'disabled');

                // For handling the progress of the upload
                myXhr.upload.addEventListener('progress', function(e) {
                    if (e.lengthComputable) {
                        $('progress').attr({
                            value: e.loaded,
                            max: e.total,
                        });
                    }
                } , false);
            }
            return myXhr;
        },
    });
});

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) { return (/^(GET|HEAD|OPTIONS|TRACE)$/).test(method); }
$(document).ready(function() {
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
});

window.crudlfap.list = function() {
    var form = $(this).parents('form');
    var data = $(this).parents('form').serialize();
    var url = window.location.pathname + '?' + data;
    var replace = '#render-table';

    // console.log(window.list_xhr);

    if (window.crudlfap.list) {
        if (window.crudlfap.list.url !== undefined && window.crudlfap.list.url == url) {
            // console.log('aborted for same url', url);
            return;
        }

        if (window.crudlfap.list.xhr !== undefined && window.crudlfap.list.xhr.state() == 'pending') {
            // console.log('aborted for obsolete', url);
            window.crudlfap.list.xhr.abort();
        }
    }
    // console.log('querying', url);

    var xhr = $.ajax({
        url: url,
    }).done(function(data, textStatus, jqXHR) {
        window.crudlfap.list = null;
        window.history.replaceState(
            null,
            $(data).find('title').html(),
            url,
        );
        $(replace).html($(data).find(replace).html());
    });

    window.crudlfap.list = {
        url: url,
        xhr: xhr,
    }
}

$(document).ready(function() {
    $('.django-filter-ajax input').keyup(window.crudlfap.list);
    $('.django-filter-ajax select').change(window.crudlfap.list);
});

