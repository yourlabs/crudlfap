import { Application } from 'stimulus'
import { definitionsFromContext } from 'stimulus/webpack-helpers'
import init from './init.js'
import M from 'materialize-css'
import './style.sass'

(() => {
  if (window.Turbolinks === undefined) {
    var Turbolinks = require('turbolinks')
    Turbolinks.start()
    Turbolinks.setProgressBarDelay(250)
  }

  // support to IE
  if (!Element.prototype.matches) {
    Element.prototype.matches = Element.prototype.msMatchesSelector ||
      Element.prototype.webkitMatchesSelector
  }

  if (!Element.prototype.closest) {
    Element.prototype.closest = function(s) {
      var el = this
      if (!document || !document.documentElement.contains(el))
        return null

      do {
        if (el.matches(s)) return el
        el = el.parentElement || el.parentNode
      } while (el != null && el.nodeType === 1)

      return el
    }
  }
}).bind(window)()

const application = Application.start()
const context = require.context('./controllers', true, /\.js$/)
application.load(definitionsFromContext(context))

// Manual controller teardown
// https://github.com/stimulusjs/stimulus/issues/104
document.addEventListener('turbolinks:before-render', function() {
  application.controllers.forEach(function(controller) {
    if(typeof controller.teardown === 'function') {
      controller.teardown()
    }
  })
})

document.addEventListener('turbolinks:before-cache', function(e) {
  // perform cleanups here
  for (var tooltip of e.target.querySelectorAll('[data-tooltip]')) {
    M.Tooltip.getInstance(tooltip).destroy()
  }
  for (var select of e.target.querySelectorAll('select')) {
    M.FormSelect.getInstance(select).destroy()
  }
})

document.addEventListener('turbolinks:load', function(e) {
  init(e.target.body)
})

document.addEventListener('click', function(e) {
  // dismiss any toast if clicking outside them
  var toast = document.getElementById('toast-container')
  if (toast && ! toast.contains(e.target)) {
    M.Toast.dismissAll()
  }

  // fixed-actions doesn't like
  var dropdowns = document.querySelectorAll('.dropdown-trigger')
  for (var dropdown of dropdowns) {
    var instance = M.Dropdown.getInstance(dropdown)
    if (instance && instance.isOpen && ! dropdown.parentElement.contains(e.target)) {
      instance.close()
    }
  }
})

const fetchers = {}

function prefetchCleanup(event) {
  clearTimeout(fetchers[event.target.href])
  event.target.removeEventListener('mouseleave', prefetchCleanup)
}

// link preload on hover poc by @hopsoft
// https://github.com/turbolinks/turbolinks/issues/313#issuecomment-407108379
document.addEventListener('mouseover', event => {
  let url = event.target.href
  if (!event.target.href) return
  clearTimeout(fetchers[url])
  if (window.Turbolinks.controller.cache.has(url)) return
  if (event.target.dataset.noprefetch) return


  event.target.addEventListener('mouseleave', prefetchCleanup)

  fetchers[url] = setTimeout(() => {
    const iframe = document.createElement('iframe')
    iframe.setAttribute('style', 'display:none')
    iframe.setAttribute('src', url)
    iframe.addEventListener('load', () => {
      window.Turbolinks.controller.cache.put(
        url,
        window.Turbolinks.Snapshot.fromHTMLElement(iframe.contentDocument.documentElement)
      )
      iframe.parentElement.removeChild(iframe)
    })
    document.body.appendChild(iframe)
  }, 250)
})

document.addEventListener('turbolinks:click', () => {
  var e = document.getElementById('main-loader')
  if (e !== undefined) {
    e.style.display = 'flex'
  }
})
document.addEventListener('turbolinks:render', () => {
  var e = document.getElementById('main-loader')
  if (e !== undefined) {
    e.style.display = 'none'
  }
})

export default application
