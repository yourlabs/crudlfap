import { Controller } from 'stimulus'
import serialize from 'form-serialize'
import init from '../init.js'

export default class extends Controller {
  input() {
    var data = serialize(this.element)
    var url = window.location.pathname + '?' + data

    Turbolinks.visit(url)
  }
}
