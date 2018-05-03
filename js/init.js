import M from 'materialize-css'

export default function(el) {
  M.AutoInit(el)
  var elems = document.querySelectorAll('.dropdown-trigger.no-autoinit')
  M.Dropdown.init(elems, {
    alignment: 'right',
    constrainWidth: false,
    coverTrigger: false,
  })
}
