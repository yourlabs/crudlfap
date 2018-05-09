import { Controller } from 'stimulus'
import Viewer from 'viewerjs'

export default class extends Controller {
  click(e) {
    e.preventDefault()

    if (!this.viewer) {
      this.viewer = new Viewer(document.getElementById(this.element.getAttribute('data-viewerjs')), {
        url: 'data-original',
      })
    }

    this.viewer.show()
  }
}
