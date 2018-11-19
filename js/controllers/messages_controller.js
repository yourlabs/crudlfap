import M from 'mrsmaterialize'
import { Controller } from 'stimulus'

export default class extends Controller {
  connect() {
    for (var el of this.element.querySelectorAll('li')) {
      M.toast({
        html: el.innerHTML,
        classes: el.getAttribute('class'),
        displayLength: 15000,
      })
      el.parentNode.removeChild(el)
    }
  }
}
