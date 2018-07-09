import { Controller } from 'stimulus'
import {MDCPersistentDrawer} from '@material/drawer'

export default class extends Controller {
  connect() {
    this.drawer.open = true
  }

  get sidenav() {
    return document.querySelector('.mdc-drawer')
  }

  get drawer() {
    if (this.sidenav.MDCPersistentDrawer) return this.sidenav.MDCPersistentDrawer
    this.sidenav.MDCPersistentDrawer = new MDCPersistentDrawer(this.sidenav)
    return this.sidenav.MDCPersistentDrawer
  }

  toggle() {
    this.drawer.open = ! this.drawer.open
  }
}
