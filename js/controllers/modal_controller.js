import Cookie from 'js-cookie'
import { Controller } from 'stimulus'
import M from 'materialize-css'
import init from '../init.js'

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
        'X-Modal': '1',
      }
    })
      .then(res => res.text())
      .catch((e) => {
        M.toast({
          html: e,
          classes: 'red darken-3',
          displayLength: 7500,
        })
      })
      .then(res => {
        var parser = new DOMParser()
        var doc = parser.parseFromString(res, 'text/html')
        var newbody = doc.getElementById('modal-body-ajax')

        var body = document.querySelector('body')
        var oldmodal = document.getElementById('modal')
        if (oldmodal) body.removeChild(oldmodal)
        this.modal = document.createElement('div')
        body.appendChild(this.modal)

        /*
        if (doc.querySelector('body.modal-fixed-footer')) {
          modal.classList.add('modal-fixed-footer')
        } else {
          modal.classList.remove('modal-fixed-footer')
        }
        */

        this.wrapper = document.createElement('div')
        this.wrapper.innerHTML = newbody.innerHTML
        this.modal.appendChild(this.wrapper)
        this.footer = this.modal.querySelector('.modal-footer')
        this.content = this.modal.querySelector('.modal-content')
        init(this.wrapper)
        this.show()
      })
  }

  show() {
    this.modal.style.display = 'block'
    this.modal.style.position = 'fixed';
    this.modal.style.zIndex = '10000';
    this.modal.style.left = '50%'
    this.modal.style.marginBottom = '10px';
    this.modal.style.transform = 'translateX(-50%)'
    this.modal.style.maxHeight = '90%'
    this.modal.setAttribute('id', 'modal')
    this.content.style.maxHeight = '90vh'
    this.content.style.maxWidth = '90vw'
    this.content.style.overflow = 'auto'
    this.startAnimation()
    this.modal.addEventListener('input', this.startAnimation.bind(this))
  }

  startAnimation() {
    this.targetMargin = (window.document.documentElement.clientHeight - this.modal.clientHeight) / 2
    if (this.targetMargin <= 10) this.targetMargin = 10
    this.currentMargin = window.document.documentElement.clientHeight
    this.raq = window.requestAnimationFrame(this.step.bind(this))
  }

  step(timestamp) {
    this.currentMargin -= 50
    this.modal.style.top = this.currentMargin + 'px'
    if (this.currentMargin >= this.targetMargin) {
      this.raq = window.requestAnimationFrame(this.step.bind(this))
    }
  }

  /*
  open() {
        var instance = M.Modal.init(this.modal, {
          preventScrolling: false,
          onOpenEnd: () => {
            this.raq = window.requestAnimationFrame(this.step.bind(this))
          }
        })
        instance.open()
  }
  step(timestamp) {
    while(this.wrapper.offsetHeight > this.modal.offsetHeight) {
      if (this.modal.offsetHeight > window.document.documentElement.clientHeight * 0.9) {
        break
      }
      debugger
      this.modal.offsetHeight += this.modal.offsetHeight * 0.1
      this.raq = window.requestAnimationFrame(this.step.bind(this))
    }
  }
  */
}
