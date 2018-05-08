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
    this.modal.style.marginBottom = '10px';
    this.modal.style.maxHeight = '90%'
    this.modal.setAttribute('id', 'modal')
    this.content.style.maxHeight = '90vh'
    this.content.style.overflow = 'auto'
    this.startAnimation()
    this.modal.addEventListener('input', this.startAnimation.bind(this))
  }

  startAnimation() {
    this.targetMarginY = (window.document.documentElement.clientHeight - this.modal.clientHeight) / 2
    if (this.targetMarginY <= 10) this.targetMarginY = 10
    this.currentMarginY = window.document.documentElement.clientHeight

    var winWidth = window.document.documentElement.clientWidth
    var modWidth = this.modal.clientWidth
    if (winWidth < modWidth * 0.9) {
      this.targetMarginX = winWidth * 0.45
    } else {
      this.targetMarginX = (winWidth - modWidth) / 2.20
    }
    this.currentMarginX = winWidth

    this.targetMarginX = (window.document.documentElement.clientWidth - this.modal.clientWidth) / 2
    if (this.targetMarginX <= 50) this.targetMarginX = 50
    this.currentMarginX = window.document.documentElement.clientWidth
    this.raq = window.requestAnimationFrame(this.step.bind(this))
  }

  step(timestamp) {
    this.modal.style.width = window.document.documentElement.clientWidth - 100
    this.modal.style.left = this.targetMarginX + 'px'
    this.modal.style.right = this.targetMarginX + 'px'
    if ((this.currentMarginY <= this.targetMarginY)) {
      return
    }
    if (this.currentMarginX >= this.targetMarginX) {
      this.currentMarginX -= 30
    }
    if (this.currentMarginY >= this.targetMarginY) {
      this.currentMarginY -= 30
    }
    this.modal.style.top = this.currentMarginY + 'px'
    this.raq = window.requestAnimationFrame(this.step.bind(this))
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
