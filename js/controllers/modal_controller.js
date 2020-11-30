import Cookie from 'js-cookie'
import { Controller } from 'stimulus'
import init from '../init.js'
import loader from '../loader.js'

export default class extends Controller {
  connect() {
    this.element.setAttribute('data-turbolinks', 'false')
  }

  get modal() {
    return document.getElementById('main-modal')
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
      var title = doc.getElementById('modal-title-ajax')
      var modalClass = this.element.getAttribute('data-modal-class')
      var modalInit = this.element.getAttribute('data-modal-init')

      // for some reason this is necessary to load the new components
      for (var script of doc.querySelectorAll('script[type=module]')) {
        var newScript = document.createElement("script");
        function loadError(oError) {
          throw new URIError("The script " + oError.target.src + " didn't load correctly.");
        }
        newScript.onerror = loadError;
        document.querySelector('head').appendChild(newScript);
        newScript.type='module'
        newScript.src = script.src;
      }

      this.modal.className = modalClass || ''
      this.modal.innerHTML = ''
      this.modal.appendChild(newbody)

      modalInit === null ? this.initmodal() : this[modalInit]()
    })
    .catch(error => {
      loader.hide()
      var snack = document.getElementById('main-snack')
      snack.labelText = error
      snack.show()
    })
  }

  initmodal() {
    init(this.modal)
    loader.hide()
    this.modal.querySelector('mwc-dialog').open = true
  }

  show() {
    init(this.modal)
    this.modal.style.display = 'block'
    this.modal.style.opacity = 1
    this.modal.style.top = null
    this.modal.style.transform = null
    this.modal.style.position = 'relative'
    loader.hide()
    for (var i of this.modal.querySelectorAll('.modal-close')) {
      i.addEventListener(
        'click',
        () => document.getElementById('modal').style.display = 'none'
      )
    }
    window.scrollTo(0, document.body.scrollHeight)
  }

  childmodal() {
    var childmodal = this.element.querySelector('.childmodal')
    this.modal.innerHTML = childmodal.innerHTML
    if (childmodal.classList.contains('modal-fixed-footer')) {
      this.modal.classList.add('modal-fixed-footer')
    } else {
      this.modal.classList.remove('modal-fixed-footer')
    }
    this.initmodal()
  }

}
