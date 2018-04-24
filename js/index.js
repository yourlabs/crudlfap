import { Application } from 'stimulus'
import { definitionsFromContext } from 'stimulus/webpack-helpers'
import M from 'materialize-css'
import 'materialize-css/sass/materialize.scss'
import './style.sass'
import CustomURLSearchParams from './search-params'

(() => {
  var Turbolinks = require('turbolinks')
  Turbolinks.start()

  // support to IE
  if (!Element.prototype.matches) {
    Element.prototype.matches = Element.prototype.msMatchesSelector ||
      Element.prototype.webkitMatchesSelector
  }

  if (!Element.prototype.closest) {
    Element.prototype.closest = function(s) {
      var el = this
      if (!document.documentElement.contains(el)) return null
      do {
        if (el.matches(s)) return el
        el = el.parentElement || el.parentNode
      } while (el != null && el.nodeType === 1)
      return el
    }
  }

  function detectIe() {
    let ua = window.navigator.userAgent
    let ie = ua.indexOf('MSIE ')

    if (ie > 0 || !!navigator.userAgent.match(/Trident.*rv:11./))
      return true
    else
      return false
  }

  if (detectIe()) {
    window['URLSearchParams'] = CustomURLSearchParams
    window['Request'] = XMLHttpRequest
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

document.addEventListener('turbolinks:load', function(e) {
  M.AutoInit(e.target.body)
})

export default application
