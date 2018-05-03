import Cookie from 'js-cookie'
import { Controller } from 'stimulus'
import M from 'materialize-css'
import init from '../init.js'

export default class extends Controller {
  connect() {
    this.element.setAttribute('data-turbolinks', 'false')
  }

  get modal() {
    return document.getElementById('modal')
  }

  open(e) {
    e.preventDefault()
    var url = this.element.getAttribute('href')
    fetch(url, {
      credentials: 'same-origin',
      headers: {
        'X-CSRFToken': Cookie.get('csrftoken'),
        'X-Modal': '1',
      }
    })
      .then(res => res.text())
      .then(res => {
        var parser = new DOMParser()
        var doc = parser.parseFromString(res, 'text/html')
        var newbody = doc.getElementById('modal-body-ajax')
        if (doc.querySelector('body.modal-fixed-footer')) {
          this.modal.classList.add('modal-fixed-footer')
        } else {
          this.modal.classList.remove('modal-fixed-footer')
        }
        this.modal.innerHTML = newbody.innerHTML
        init(this.modal)

        var instance = M.Modal.init(document.getElementById('modal'), {
          preventScrolling: false,
        })
        instance.open()
      })
  }
}
