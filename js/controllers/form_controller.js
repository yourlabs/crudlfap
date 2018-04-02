import Cookie from 'js-cookie'
import M from 'materialize-css'
import { Controller } from 'stimulus'

export default class extends Controller {
  submit(e) {
    e.preventDefault()
    var url = this.element.getAttribute('action')
    var formData = new FormData(this.element)

    var req = new Request(url)
    fetch(req, {
      credentials: 'same-origin',
      body: formData,
      redirect: 'manual',
      method: 'POST',
      headers: {
        'X-CSRFToken': Cookie.get('csrftoken'),
        'Cache-Control': 'no-cache',
      }
    })
    .then(res => require('turbolinks').visit(res.headers['Location']))
  }
}
