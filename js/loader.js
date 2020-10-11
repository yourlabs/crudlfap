
var loader = {}

loader.show = () => {
  var e = document.getElementById('main-loader')
  if (e !== undefined) {
    e.style.display = 'flex'
  }
}

loader.hide = () => {
  for (var e of document.getElementsByClassName('loader-container')) {
    e.style.display = 'none'
  }
}

export default loader
