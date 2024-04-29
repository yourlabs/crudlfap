import { Controller } from '@hotwired/stimulus'
import serialize from 'form-serialize'
import init from '../init.js'

export default class extends Controller {
  input() {
    var data = serialize(this.element)
    var url = window.location.pathname + '?' + data

    if (this.url !== undefined) {
      if (this.url === url) {
        // console.log('aborted for same url', url);
        return
      }
      if (this.xhr !== undefined && this.xhr.readyState < 4) {
        this.xhr.abort()
      }
    }

    this.url = url
    this.xhr = new XMLHttpRequest()
    this.xhr.open('GET', this.url)
    this.xhr.onload = this.onload.bind(this)
    this.xhr.send()
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
