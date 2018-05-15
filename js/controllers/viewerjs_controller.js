import { Controller } from 'stimulus'
import Viewer from 'viewerjs'

export default class extends Controller {
  click(e) {
    e.preventDefault()
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
      document.body.appendChild(viewer)
    }
    return viewer
  }

  get viewerOptions() {
    return {
      url: 'data-original',
    }
  }

  get viewer() {
    if (this.viewerObject === undefined) {
      this.viewerObject = new Viewer(this.viewerElement, this.viewerOptions)
    }
    return this.viewerObject
  }
}
