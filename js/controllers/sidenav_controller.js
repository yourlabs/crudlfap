import { Controller } from '@hotwired/stimulus'
import M from '@materializecss/materialize'

export default class extends Controller {
  /* As awesome as it is, it doesn't even initialize the
   * sidebar until a user clicks the menu.
   */
  click() {
    if (this.instance === undefined) {
      M.Sidenav.init(this.sidenav).open()
    }
  }

  teardown() {
    if (this.instance !== undefined) {
      this.instance.destroy()
    }
  }

  get sidenav() {
    if (this.element === undefined) return undefined
    return document.getElementById(this.element.getAttribute('data-target'))
  }

  get instance() {
    return M.Sidenav.getInstance(this.sidenav)
  }
}
