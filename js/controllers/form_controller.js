import Cookie from 'js-cookie'
import { Controller } from 'stimulus'
import M from 'materialize-css'

export default class extends Controller {
  submit(e) {
    if (this.element.id === undefined) {
      // console.warn('Skipping ajax because form tag has no id attr')
      return
    }
    e.preventDefault()
    var url = this.element.getAttribute('action')
    var formData = new FormData(this.element)

    var application = this.application
    var req = new Request(url)
    fetch(req, {
      credentials: 'same-origin',
      body: formData,
      redirect: 'manual',
      method: 'POST',
      headers: {
        'X-CSRFToken': Cookie.get('csrftoken'),
        'Cache-Control': 'no-cache',
      }
    }).then(res => {
      if (res.type == 'opaqueredirect') {
        window.Turbolinks.visit(res.headers['Location'])
      }

      res.text().then(text => {
        var parser = new DOMParser()
        var doc = parser.parseFromString(text, 'text/html')
        var newForm = doc.getElementById(this.element.id)

        // In case we find the same form in the response, we refresh only the
        // form tag, this works both inside modal and in normal page view.
        var source, target
        if (newForm) {
          source = newForm
          target = this.element
        } else {
          source = doc.querySelector('body')
          target = document.querySelector('body')
        }

        application.controllers.forEach(function(controller) {
          if(target.contains(controller.element) && typeof controller.teardown === 'function') {
            controller.teardown()
          }
        })
        target.innerHTML = source.innerHTML
        M.AutoInit(target)
      })
    })
  }
}
