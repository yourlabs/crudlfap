import M from 'materialize-css'
import { Controller } from 'stimulus'

export default class extends Controller {
  connect() {
    if (document.body.classList.contains('listaction-ready')) return
    this.actionbarDisplay()
    document.body.classList.add('listaction-ready')
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
  }
  actionbarDisplay() {
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
