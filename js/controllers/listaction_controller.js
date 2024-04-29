import queryString from 'query-string'
import { Controller } from '@hotwired/stimulus'

export default class extends Controller {
  connect() {
    var cls = document.body.getAttribute('class')
    if (cls.indexOf('listaction-ready') > -1) return
    this.actionbarDisplay()
    this.urlUpdate()
    document.body.setAttribute('class', cls + ' listaction-ready')
  }
  get checkboxes() {
    return Array.prototype.slice.call(document.querySelectorAll('table input[type=checkbox][data-pk]'))
  }
  get leader() {
    return document.querySelector('table input[type=checkbox][data-master]')
  }
  get actionbar() {
    return document.getElementById('listaction')
  }
  checkboxChange() {
    if (this.leader.checked && !this.element.checked) {
      this.leader.checked = false
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
    }
    this.checkboxChange()
  }
  showActions() {
    document.getElementById('listactions')
  }
}
