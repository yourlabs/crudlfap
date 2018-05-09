import Cookie from 'js-cookie'
import { Controller } from 'stimulus'
import M from 'materialize-css'
import init from '../init.js'

function pair(num) {
  return num % 2 == 0 ? num : num - 1
}

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
        // disconnect any existing observer
        if (this.observer !== undefined) {
          this.observer.disconnect()
        }

        // remove old modal if any
        var oldmodal = document.getElementById('modal')
        if (oldmodal) document.body.removeChild(oldmodal)

        // parse new modal content from response
        var parser = new DOMParser()
        var doc = parser.parseFromString(res, 'text/html')
        var newbody = doc.getElementById('modal-body-ajax')

        // create modal element
        this.modal = document.createElement('div')

        // mount content in modal
        this.content = newbody.querySelector('.modal-content')
        this.modal.appendChild(this.content)

        // mount footer in modal
        this.modal.appendChild(newbody.querySelector('.modal-footer'))
        this.footer = this.modal.querySelector('.modal-footer')

        // apply styles
        this.modal.setAttribute('id', 'modal')
        this.modal.style.position = 'fixed'
        this.modal.style.padding = '12px'
        this.modal.style.zIndex = '10000'
        this.modal.style.backgroundColor = '#DDDDDD'

        this.content.style.overflow = 'auto'
        this.content.style.backgroundColor = '#AAAAAA'

        // mount modal in body
        document.body.appendChild(this.modal)

        // proceed our initialization of elements
        init(this.wrapper)

        // mount resize observer
        this.observer = new MutationObserver(this.decayObserve.bind(this))
        this.observer.observe(this.modal, {
            attributes: true,
            characterData: true,
            childList: true,
            subtree: true,
        })

        // reset margins
        this.margin = {
          top: 50,
        }

        this.margin.bottom = this.browserHeight - this.footerHeight - this.contentHeight - this.margin.top
        if (this.margin.bottom < 50) this.margin.bottom = 50
        console.log(this.browserHeight,this.footerHeight,this.contentHeight,this.margin.top,this.margin.bottom)

        this.margin.left = (this.browserWidth - this.contentWidth) / 2
        if (this.margin.left < 50) this.margin.left = 50

        this.margin.right = this.browserWidth - this.contentWidth - this.margin.left
        if (this.margin.right < 50) this.margin.right = 50

        // show modal, should trigger observer
        this.modal.style.display = 'block'
      })
  }

  decayObserve() {
    if (this.oldContentWidth == this.contentWith && this.oldContentHeight == this.contentHeight) return
    if (this.timeout) window.clearTimeout(this.timeout)
    this.timeout = window.setTimeout(this.observe.bind(this), 50)
  }

  observe() {
    this.margin.bottom = this.browserHeight - this.footerHeight - 50 * 2 - this.contentHeight - this.margin.top
    if (this.raq) window.cancelAnimationFrame(this.raq)
    this.raq = window.requestAnimationFrame(this.resize.bind(this))
  }

  resize() {
    console.log('resize')
    var maxHeight = (this.browserHeight - this.footerHeight - 50 * 2) + 'px'
    if (this.content.style.maxHeight != maxHeight)
      this.content.style.maxHeight = maxHeight

    var maxWidth = (this.browserWidth - 50 * 2) + 'px'
    if (this.content.style.maxWidth != maxHeight)
      this.content.style.maxWidth = maxHeight

    var top = this.margin.top + 'px'
    if (this.modal.style.top != top) this.modal.style.top = top

    var bottom = this.margin.bottom + 'px'
    if (this.modal.style.bottom != bottom) this.modal.style.bottom = bottom

    var right = this.margin.right + 'px'
    if (this.modal.style.left != left) this.modal.style.left = left

    var left = this.margin.left + 'px'
    if (this.modal.style.right != right) this.modal.style.right = right

    this.oldContentHeight = this.contentHeight
    this.oldContentWidth = this.contentWidth
    this.raq = false
  }

  get bottomMargin() {
    var result = this.browserHeight - this.footerHeight - 50 * 2 - this.margin.top - this.contentHeight
    return result > this.bottomMinMargin ? result : this.bottomMinMargin
  }

  get bottomMinMargin() {
    return 50 + this.footerHeight
  }

  get topMargin() {
    var result = this.browserWidth - 50 * 2 - this.margin.left - this.contentWidth
    return result > 50 ? result : 50
  }

  get browserHeight() {
    return window.document.documentElement.clientHeight
  }

  get browserWidth() {
    return window.document.documentElement.clientHeight
  }

  get contentHeight() {
    return this.content.clientHeight
  }

  get contentMaxHeight() {
    return this.browserHeight - 50 * 2 - this.footer.clientHeight
  }

  get contentWidth() {
    return this.content.clientWidth
  }

  get contentMaxWidth() {
    return this.browserWidth - 50 * 2
  }

  get footerHeight() {
    return this.footer.clientHeight
  }

  show() {
    if (this.raq) window.cancelAnimationFrame(this.raq)

    if (Object.keys(this.margin).length && this.clientHeight - this.margin.top - this.margin.bottom >= this.contentHeight) {
      this.margin.bottom = this.clientHeight - this.margin.top - this.contentHeight
      console.log('touching bottom')
    } else {  // grow
      this.margin.top = this.margin.bottom = parseInt((this.clientHeight - this.contentHeight) / 2)
      console.log('touching top and bottom')
    }
    console.log('after', this.contentHeight, this.margin, this.modal.style.top, this.modal.style.bottom)

    if (this.margin.left && this.margin.right && this.clientWidth - this.margin.left - this.margin.right >= this.content.clientWidth) {
      this.margin.right = this.clientWidth - this.content.clientWidth - this.margin.left
    } else {
      this.margin.right = this.margin.left = parseInt((this.clientWidth - this.content.clientWidth) / 2)
    }

    if (this.margin.top < 50) this.margin.top = 50
    if (this.margin.bottom < 50) this.margin.bottom = 50
    if (this.margin.left < 50) this.margin.left = 50
    if (this.margin.right < 50) this.margin.right = 50

    this.raq = window.requestAnimationFrame(this.resize.bind(this))

  }
}
