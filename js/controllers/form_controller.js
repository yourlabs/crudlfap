import Cookie from 'js-cookie'
import { Controller } from 'stimulus'
import init from '../init.js'
import loader from '../loader.js'

export default class extends Controller {
  triggerSubmit(e) {
    var form

    // try parents
    var parentNode = e.target.parentNode
    while (parentNode && parentNode.tagName != 'FORM' && parentNode.parentNode)
      var parentNode = parentNode.parentNode

    // then try previous siblings
    if (parentNode.tagName == 'FORM') {
      form = parentNode
    } else {
      var current = e.target.previousElementSibling
        debugger;
      while (current && current.tagName != 'FORM' && current.previousElementSibling)
        current = current.previousElementSibling
      if (current && current.tagName == 'FORM') {
        form = current
      } else {
	    // try form attribute -
    	if (e.target.hasAttribute('form')) {
    		var formId = e.target.getAttribute('form')
	    	form = document.getElementById(formId)
	    } else {
	    	throw 'err: form element not found.'
	    }
      }
    }

    var event = new Event('submit', {
        'bubbles'    : true, // Whether the event will bubble up through the DOM or not
        'cancelable' : true  // Whether the event may be canceled or not
    });
    form.dispatchEvent( event );
  }

  submit(e) {
    if (this.element.id === undefined) {
      // console.warn('Skipping ajax because form tag has no id attr')
      return
    }
    loader.show()
    e.preventDefault()
    var url = this.element.getAttribute('action')
    var formData = new FormData(this.element)
    for (var input of this.element.querySelectorAll('[name]')) {
      if (formData.has(input.attributes.name)) continue
      formData.set(input.name, input.value)
    }

    var application = this.application
    fetch(url, {
      credentials: 'same-origin',
      body: formData,
      method: 'POST',
      headers: {
        'X-CSRFToken': Cookie.get('csrftoken'),
        'Cache-Control': 'no-cache',
      }
    }).then(res => {
      return res.text()
    }).then(text => {
      var parser = new DOMParser()
      var doc = parser.parseFromString(text, 'text/html')
      var newForm = doc.getElementById(this.element.id)

      // In case we find the same form in the response, we refresh only the
      // form tag, this works both inside modal and in normal page view.
      var source, target, url, title
      if (newForm) {
        source = newForm
        target = this.element
      } else {
        source = doc.querySelector('body')
        target = document.querySelector('body')
        var canonical = doc.querySelector('link[rel=canonical]')
        if (canonical) {
          url = canonical.getAttribute('href')
        }
        title = doc.querySelector('title').innerHTML

        // we're going to replace the body, that means we close the modal
        // which will restore the browser scrollbars if any
        document.getElementById('main-modal').querySelector('mwc-dialog').open = false
      }

      /**
       * Tear down controller before removing HTML
       */
      application.controllers.forEach(function(controller) {
        if(target.contains(controller.element) && typeof controller.teardown === 'function') {
          controller.teardown()
        }
      })

      target.innerHTML = source.innerHTML

      init(target)
      loader.hide()

      if (url && url != window.location.href) {
        window.history.pushState({}, title, url)
      }
    }).catch(error => {
      loader.hide()
        /*
      M.toast({
        html: error,
        classes: 'orange darken-4',
        displayLength: 15000,
      })
      */
    })
  }
}
