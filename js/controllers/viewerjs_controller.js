import { Controller } from '@hotwired/stimulus'
import Viewer from 'viewerjs'

export default class extends Controller {
  connect() {
    if (this.viewerElement === null) {
      this.createViewerElement()
      new Viewer(this.viewerElement, this.viewerOptions)
    }
  }

  click(e) {
    e.preventDefault()
    this.viewerElement.querySelector('[data-original="' + this.element.getAttribute('href') + '"]').click()
  }

  createViewerElement() {
    // no web component for me, damn you ie
    var container = document.createElement('div')
    var viewer = document.createElement('ul')
    viewer.setAttribute('id', this.viewerId)
    viewer.style.display = 'none'
    for (var image of this.images) {
      var img = document.createElement('img')
      img.setAttribute('data-original', image.getAttribute('href'))
      img.setAttribute('src', image.getAttribute('href'))
      img.setAttribute('alt', image.text)
      var item = document.createElement('li')
      item.appendChild(img)
      viewer.appendChild(item)
    }
    container.appendChild(viewer)
    document.body.appendChild(container)
  }

  get images() {
    return document.querySelectorAll('[data-viewerjs=' + this.viewerName + ']')
  }

  get viewerName() {
    return this.element.getAttribute('data-viewerjs')
  }

  get viewerId() {
    return 'viewerjs-' + this.viewerName
  }

  get viewerElement() {
    return document.getElementById(this.viewerId)
  }

  get viewerOptions() {
    return {
      url: 'data-original',
    }
  }
}
