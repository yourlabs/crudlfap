import M from 'materialize-css'
import { Controller } from 'stimulus'

export default class extends Controller {
  connect() {
    for (var el of this.element.querySelectorAll('li')) {
      M.toast({
        html: el.innerHTML,
        classes: el.getAttribute('class'),
      })
      el.parentNode.removeChild(el)
    }
  }
}
