import { Controller } from 'stimulus'
import Viewer from 'viewerjs'

export default class extends Controller {
  click(e) {
    e.preventDefault()
    this.viewer = new Viewer(this.viewerElement, this.viewerOptions)
    this.viewer.show()
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
    var viewer = document.getElementById(this.viewerId)
    if (!viewer) {
      // no web component for me, damn you ie
      var container = document.createElement('div')
      viewer = document.createElement('ul')
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
    return viewer
  }

  hidden() {
    this.viewer.destroy()
  }

  get viewerOptions() {
    return {
      url: 'data-original',
      hidden: this.hidden.bind(this),
    }
  }
}
