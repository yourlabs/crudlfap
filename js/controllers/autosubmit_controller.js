import { Controller } from 'stimulus'
import serialize from 'form-serialize'
import init from '../init.js'

export default class extends Controller {
  input() {
    // clear any xhr planner
    this.timeoutId && window.clearTimeout(this.timeoutId)
    // clear any unsent xhr
    this.xhr && this.xhr.readyState === 0 && this.xhr.abort()

    var data = serialize(this.element)
    for (var input of this.element.querySelectorAll('[name]')) {
      if (input.value === undefined) continue
      data += '&' + input.getAttribute('name') + '=' + input.value
    }

    this.xhr = new XMLHttpRequest()
    this.xhr.open('GET', window.location.pathname + '?' + data)
    this.xhr.onload = this.onload.bind(this)
    // plan an xhr
    this.timeoutId = window.setTimeout(() => this.xhr.send(), 250)
  }

  onload(e) {
    var parser = new DOMParser()
    var doc = parser.parseFromString(e.target.responseText, 'text/html')
    var target = document.getElementById(this.targetId)
    target.innerHTML = doc.getElementById(this.targetId).innerHTML
    init(target)
    window.history.pushState({turbolinks: {}}, doc.querySelector('title').innerHTML, this.url)
  }

  get targetId() {
    return this.element.getAttribute('data-target')
  }
}
