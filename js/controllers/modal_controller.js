import Cookie from 'js-cookie'
import M from 'materialize-css'
import { Controller } from 'stimulus'

export default class extends Controller {
  connect() {
    this.element.setAttribute('data-turbolinks', 'false')
  }
  open(e) {
    e.preventDefault()
    var url = this.element.getAttribute('href')
    fetch(url, {
      credentials: 'same-origin',
      headers: {
        'X-CSRFToken': Cookie.get('csrftoken'),
      }
    })
      .then(res => res.text())
      .then(res => {
        var parser = new DOMParser()
        var doc = parser.parseFromString(res, 'text/html')
        document.getElementById('modal-body').innerHTML = doc.getElementById('modal-body-ajax').innerHTML
        M.AutoInit(document.getElementById('modal'))
        var instance = M.Modal.init(document.getElementById('modal'))
        instance.open()
      })
  }
}
