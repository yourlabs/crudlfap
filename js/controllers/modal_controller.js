import Cookie from 'js-cookie'
import { Controller } from 'stimulus'
import M from 'materialize-css'
import init from '../init.js'
import Dialog from 'react-toolbox/lib/dialog'
import React from 'react'
import ReactDOM from 'react-dom'


class DialogTest extends React.Component {
  state = {
    active: false
  };

  handleToggle = () => {
    this.setState({active: !this.state.active});
  }

  actions = [
    { label: "Cancel", onClick: this.handleToggle },
    { label: "Save", onClick: this.handleToggle }
  ];

  render () {
    return (
      <div>
        <Button label='Show my dialog' onClick={this.handleToggle} />
        <Dialog
          actions={this.actions}
          active={this.state.active}
          onEscKeyDown={this.handleToggle}
          onOverlayClick={this.handleToggle}
          title='My awesome dialog'
        >
          <p>Here you can add arbitrary content. Components like Pickers are using dialogs now.</p>
        </Dialog>
      </div>
    )
  }
}



export default class extends Controller {
  connect() {
    this.element.setAttribute('data-turbolinks', 'false')

  }

  get modal() {
    return document.getElementById('modal')
  }

  open(e) {
    e.preventDefault()
    var elem = document.createElement('div')
    document.body.appendChild(elem)
    ReactDOM.render(DialogTest, elem)
    var url = this.element.getAttribute('href')
    fetch(url, {
      credentials: 'same-origin',
      headers: {
        'X-CSRFToken': Cookie.get('csrftoken'),
        'X-Modal': '1',
      }
    })
      .then(res => res.text())
      .then(res => {
        var parser = new DOMParser()
        var doc = parser.parseFromString(res, 'text/html')
        var newbody = doc.getElementById('modal-body-ajax')
        if (doc.querySelector('body.modal-fixed-footer')) {
          this.modal.classList.add('modal-fixed-footer')
        } else {
          this.modal.classList.remove('modal-fixed-footer')
        }
        this.modal.innerHTML = newbody.innerHTML
        init(this.modal)

        var instance = M.Modal.init(document.getElementById('modal'), {
          preventScrolling: false,
        })
        instance.open()
      })
  }
}
