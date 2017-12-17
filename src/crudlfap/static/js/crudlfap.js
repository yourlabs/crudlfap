import $ from 'jquery'
import mdc from 'material-components-web'

(() => {
  // datepicker needs jquery names `jQuery` in window global namespace
  window.jQuery = $
  // Materialize needs jquery names `$` in window global namespace
  window.$ = $

  mdc.autoInit()

})()
