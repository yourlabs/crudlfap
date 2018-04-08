import { Controller } from 'stimulus'

export default class extends Controller {
  input() {
    var data = new FormData(this.element)
    var query = new URLSearchParams(data)
    var url = window.location.pathname + '?' + query.toString()

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
    document.getElementById(this.targetId).innerHTML = doc.getElementById(this.targetId).innerHTML
  }

  get targetId() {
    return this.element.getAttribute('data-target')
  }
}
