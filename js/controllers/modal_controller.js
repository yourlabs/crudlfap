import Cookie from 'js-cookie'
import { Controller } from 'stimulus'
import M from 'mrsmaterialize'
import init from '../init.js'
import loader from '../loader.js'

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
    loader.show()
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
      var modalClass = this.element.getAttribute('data-modal-class')
      var modalInit = this.element.getAttribute('data-modal-init')
      this.modal.className = modalClass === null ? 'modal fade' : modalClass
      this.modal.innerHTML = newbody.innerHTML
      loader.hide()
      modalInit === null ? this.initmodal() : this[modalInit]()
    }).catch(error => {
      loader.hide()
      M.toast({
        html: error,
        classes: 'orange darken-4',
        displayLength: 15000,
      })
    })
  }

  initmodal() {
    init(this.modal)
    var instance = M.Modal.init(document.getElementById('modal'), {
      endingTop: '5%',
    })
    instance.open()
  }

  show() {
    init(this.modal)
    this.modal.style.display = 'block'
    this.modal.style.opacity = 1
    this.modal.style.top = null
    this.modal.style.transform = null
    this.modal.style.position = 'relative'
    window.scrollTo(0, document.body.scrollHeight)
  }
}
