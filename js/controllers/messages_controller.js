import { Controller } from '@hotwired/stimulus'
import M from '@materializecss/materialize'

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
