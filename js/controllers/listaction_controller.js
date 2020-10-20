import queryString from 'query-string'
import { Controller } from 'stimulus'

export default class extends Controller {
  connect() {
    var cls = document.body.getAttribute('class')
    if (cls.indexOf('listaction-ready') > -1) return
    this.actionbarDisplay()
    this.urlUpdate()
    document.body.setAttribute('class', cls + ' listaction-ready')
  }
  get checkboxes() {
    return Array.prototype.slice.call(document.querySelectorAll('table [data-action="change->listaction#checkboxChange"]'))
  }
  get leader() {
    return document.querySelector('table [data-action="change->listaction#selectAllChange"]')
  }
  get actionbar() {
    return document.getElementById('listaction')
  }
  checkboxChange() {
    let total = this.checkboxes.length
    let checked = this.checkboxes.filter((item) => item.checked).length

    if (checked) {
      if (checked == total) {
        this.leader.checked = true
      } else {
        this.leader.indeterminate = true
      }
    } else {
      this.leader.indeterminate = false
      this.leader.checked = false
    }

    if (this.element.checked) {
      this.element.parentNode.parentNode.classList.add('selected')
    } else {
      this.element.parentNode.parentNode.classList.remove('selected')
    }

    this.actionbarDisplay()
    this.urlUpdate()
  }
  urlUpdate() {
    var pks = []
    for (var c of this.checkboxes) {
      if (c.checked) {
        pks.push(c.getAttribute('data-pk'))
      }
    }
    var links = document.querySelectorAll('[data-listaction=urlupdate]')
    for (var link of links) {
      if (! link.hasAttribute('data-listaction-origurl')) {
        link.setAttribute('data-listaction-origurl', link.getAttribute('href'))
      }

      link.setAttribute('href', link.getAttribute('data-listaction-origurl') + '?' + queryString.stringify({pks: pks}))
    }
  }
  actionbarDisplay() {
    // some race condition in opera ? Sentry betagouv/mrs issue #269
    if (!this.actionbar) return

    if (this.checkboxes.filter(a => a.checked).length)
      this.actionbar.style.display = 'inline-block'
    else
      this.actionbar.style.display = 'none'
  }
  selectAllChange() {
    for (var cb of this.checkboxes) {
      cb.checked = this.element.checked
      if (cb.checked) {
        cb.parentNode.parentNode.classList.add('selected')
      } else {
        cb.parentNode.parentNode.classList.remove('selected')
      }
    }
    this.checkboxChange()
  }
  showActions() {
    document.getElementById('listactions')
  }
}
