var crudlfap = crudlfap || {}

crudlfap.Ajax = function(url, method, data, callback, options) {
    if (crudlfap.state && crudlfap.state.DEBUG) {
        console.log('Ajax(', method, url, data, callback, options)
    }

    this.callback = callback
    this.options = options
    this.uploading = data instanceof FormData ? true : false;

    $.ajax({
        url: url,
        type: method,
        data: data,

        // Tell jQuery not to process data or worry about content-type
        // You *must* include these options for HTML5 uploads !
        contentType: !this.uploading,
        processData: !this.uploading,
        cache: !this.uploading,

        beforeSend: function(xhr) {
            xhr.setRequestHeader('Cache-Control', 'no-cache');
        },
        complete: $.proxy(this.complete, this),
        error: $.proxy(this.error, this),
        xhr: this.xhr,
    });
}

crudlfap.Ajax.prototype.complete = function(jqXHR) {
    var $data = $(jqXHR.responseText);

    // Update global state object
    try {
        crudlfap.state = JSON.parse($data.filter('#ajax-state').html())
    } catch(e) {
        if (console) console.log('Could not parse ajax state')
        crudlfap.state = false
    }
    crudlfap.state.title = $data.filter('title').html()

    this.callback($data, this.options, jqXHR);
}

crudlfap.Ajax.prototype.error = function(jqXHR) {
    if (crudlfap.state && crudlfap.state.DEBUG) {
        $('body').html($(jqXHR.responseText).filter('body').html());
    }
}

crudlfap.Ajax.prototype.xhr = function() {
    var myXhr = $.ajaxSettings.xhr();

    if (myXhr.upload) {
        // Disable everything during upload
        $('#modal :input').attr('disabled', 'disabled');

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
}

crudlfap.completePage = function($data, options, jqXHR) {
    if (crudlfap.state && crudlfap.state.ajax) {
        $(crudlfap.state.ajax).each(function() {
            var id = $(this).attr('id');
            if (id === undefined) {
                if (console) {
                    console.log('Skipping update of element lacking id', $(this))
                }
                return
            }
            id = '#' + id
            var source = $data.filter(id);
            if (!source.length) source = $data.find(id)
            if (!source.length) return

            var target = $(id);
            if (!target.length) return

            target.html(source.html())
        });
    }

    $('title').html(crudlfap.state.title);

    if (options.history) {
        window.history.pushState(
            null,
            crudlfap.state.title,
            crudlfap.state.url,
        );
    }
}

crudlfap.completeModal = function($data, options, jqXHR) {
    // Fill in Modal
    /*
    $('#modal .modal-content').removeClass(function (index, className) {
        return (className.match (/(^|\s)panel-\S+/g) || []).join(' ');
    }).addClass('panel-' + crudlfap.state.style);

    $('#modal .modal-title').removeClass(function (index, className) {
        return (className.match (/(^|\s)text-\S+/g) || []).join(' ');
    }).addClass('text-' + crudlfap.state.style);
    */

    $('#modal .modal-body').html($data.find('#modal-body-ajax').html())
    $('#modal .modal-body-ajax').prepend($data.find('#messages'));
    $('#modal .modal-title').html($data.find('#modal-title-ajax').html());
    $('#modal').modal({
      	dismissible: true,
		opacity: .5,
		inDuration: 300, // Transition in duration
        outDuration: 200, // Transition out duration
        startingTop: '4%', // Starting top style attribute
        endingTop: '10%', // Ending top style attribute
        ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
            alert("Ready");
            console.log(modal, trigger);
        },
        complete: function() { alert('Closed'); } // Callback for Modal close

    });
    console.log('modalcomplete !')
}

crudlfap.completeForm = function($data, options, jqXHR) {
    // Update form and messages in modal, or close modal and update DOM
    var $form = $data.find('#' + options.formId)
    if (!$form.length) $form = $data.filter('#' + options.formId)
    if ($form.length) {
        // Form is still there, display again
        $('#' + options.formId).html($form.html())
    } else {
        // Form is gone, load page
        crudlfap.completePage($data, {history: true}, jqXHR)
        $('#modal').modal('hide')
    }
}

/* Intercept clicks to ajaxify requests.
 *
 * Do nothing if href starts with '#', open link in a modal if
 * data-target=model.
 */
$('body').on('click', 'a[data-ajax]', function(e) {
    e.preventDefault();
    var $e = $(this);
    var options = {}
    var callback
    if ($(this).attr('data-ajax') == '_modal') {
        callback = crudlfap.completeModal
        options.history = false
    } else {
        callback = crudlfap.completePage
        options.history = true
    }

    try {
        var data = JSON.parse($(this).attr('data-ajax-data'))
    } catch (e) {
        var data = null
    }

    new crudlfap.Ajax(
        $(this).attr('href'),
        $(this).attr('data-ajax-method') || 'GET',
        data,
        callback,
        options
    )
});

// Support history back/forward
window.onpopstate = function(event) {
    new crudlfap.Ajax(
        document.location.href,
        'GET',
        {},
        crudlfap.completePage
    )
};

// Focus on first input when opening modal
$('body').on('shown.bs.modal', function (e) {
    $(e.target).find(':input:first').focus()
;
});

/* Intercept submits to ajaxify requests.
 */
$('body').on('submit', 'form[data-ajax]', function(e) {
    e.preventDefault();

    var form = $(this);

    // Get form data before disabling fields
    var formData = new FormData(form[0])

    // Disable inputs to prevent double posting ... 2017 FTW <3
    form.find(':input').attr('disabled', 'disabled');

    // Show form loading div
    form.find('.form-loading').show();

    new crudlfap.Ajax(
        $(this).attr('action'),
        $(this).attr('method') || 'POST',
        formData,
        crudlfap.completeForm,
        {
            formId: form.attr('id')
        }
    )
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
    try {
        crudlfap.state = JSON.parse($('#ajax-state').html())
    } catch (e) {
        if (console) console.log('Could not parse ajax state', e)
        crudlfap.state = false
    }
    crudlfap.state.title = $('title').html()

    $('body').on('keyup', '.django-filter-ajax input', window.crudlfap.list);
    $('body').on('change', '.django-filter-ajax select', window.crudlfap.list);

    // sidebar
    $('.button-collapse').sideNav();
});

