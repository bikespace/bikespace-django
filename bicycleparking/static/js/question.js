import TextInput from './types/text';
import StringInput from './types/string';
import DateTimeInput from './types/date';
import LatLngInput from './types/latlng';
import types from './types/types';

export default class Question {
  constructor(props, survey) {
    this.props = props;
    this.survey = survey;
    const question = {
      submit: this.submit.bind(this),
      onError: this.onError.bind(this),
      onMessage: this.onMessage.bind(this),
      router: this.survey.router
    }
    if (this.props.type === 'DATETIME') {
      this.input = new DateTimeInput(props, question)
    } else if (this.props.type === 'TEXT') {
      this.input = new TextInput(props, question)
    } else if (this.props.type === types.LATLNG) {
      this.input = new LatLngInput(props, question)
    } else {
      this.input = new StringInput(props, question)
    }
  }

  submit(value) {
    if (value) {
      this.survey.setState({
        [this.props.key]: value
      })
    }
    if (this.props.final) {
      this.survey.submit();
    } else if (value) {
      this.survey.navigate()
    } else {
      if (this.props.required) {
        this.error.innerHTML = 'Please fill out this value'
      } else {
        this.survey.navigate()
      }
    }
  }

  onError(error) {
    this.error.text = error;
  }

  onMessage(message) {
    this.message.text = message;
  }

  render() {
    this.el = this.el || document.getElementById('render');
    this.el.innerHTML = this.template();
    this.el.className = '';
    this.el.classList.add(this.props.key)
    this.error = document.getElementById('error');
    this.message = document.getElementById('message');
    this.input.bind();
  }
  
  template() {
    return (
      `
      <div class="View">
        <div class="Step ${this.props.key}">
          <h1 class="Step__heading">${this.props.heading}</h1>
          <p class="Step__text">${this.props.text}</p>
          ${this.input.template}
          <p id="error" class="Step__error"></p>
          <p id="message" class="Step__message"></p>
        </div>
        </div>
      `
    )
  }
}