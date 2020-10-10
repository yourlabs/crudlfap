// clean up behind materialize

import M from 'mrsmaterialize'

export default function(el) {
  M.AutoInit(el)
  var elems = el.querySelectorAll('.dropdown-trigger.no-autoinit')
  M.Dropdown.init(elems, {
    alignment: 'right',
    constrainWidth: false,
    coverTrigger: true,
  })
  for (let element of el.querySelectorAll('.crudlfap-datepicker')) {
    M.Datepicker.init(element, {
      showClearBtn: element.getAttribute('data-clearable'),
      format: element.getAttribute('data-format'),
    })
  }

  for (let element of el.querySelectorAll('textarea')) {
    M.textareaAutoResize(element)
  }

  for (let element of el.querySelectorAll('input')) {
    M.updateTextFields()
  }

  // compensate for https://github.com/Dogfalo/materialize/issues/6049
  for (let select of el.querySelectorAll('select.invalid')) {
    try {
      var input = select.previousSibling.previousSibling.previousSibling
    } catch (error) {
      continue
    }
    if (input.classList) {
      input.classList.add('invalid')
    }
  }
}
