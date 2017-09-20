import TextInput from './types/text';
import StringInput from './types/string';
import DateTimeInput from './types/date';
import LatLngInput from './types/latlng';
import ArrayInput from './types/array';
import SelectInput from './types/select';
import ImageInput from './types/image';
import types from './types/types';

export default class Pane {
  constructor(props, survey) {
    this.props = props;
    this.survey = survey;
    const question = {
      submit: this.submit.bind(this),
      onError: this.onError.bind(this),
      onMessage: this.onMessage.bind(this),
      router: this.survey.router
    }
    this.questions = this.props.questions.map((q) => {
      return this.createInput(q, question)
    });
  }

  createInput(props, question) {
    if (props.type === types.DATETIME) {
      return new DateTimeInput(props, question)
    } else if (props.type === types.TEXT) {
      return new TextInput(props, question);
    } else if (props.type === types.LATLNG) {
      return new LatLngInput(props, question);
    } else if (props.type === types.ARRAY) {
      return new ArrayInput(props, question);
    } else if (props.type === types.IMAGE) {
      return  new ImageInput(props, question);
    } else if (props.type === types.STRING && props.values && props.values.length) {
      return new SelectInput(props, question);
    } else {
      return new StringInput(props, question);
    }
  }

  submit() {
    const values = this.questions.reduce((memo, question) => {
      memo[question.props.key] = question.value;
      return memo;
    }, {})

    if (values) {
      this.survey.setState(values)
    }
    if (this.props.final) {
      this.survey.submit();
    } else if (values) {
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
    this.bind();
  }
   
  get canSkip() {
    return this.props.questions.reduce((memo, question) => {
      if (question.required) {
        memo = false;
      }
      return memo;
    }, true);
  }
  
  bind() {
    document.getElementById('button').addEventListener('click', (event) => {
      this.submit();
    });

    if (this.canSkip) {
      document.getElementById('skip').addEventListener('click', (event) => {
        this.submit(null);
      });
    }
    this.questions.forEach((question) => {
      question.bind();
    })
  }

  template() {
    const templates = this.questions.reduce((memo, question) => {
      memo += question.template;
      return memo;
    }, '')
    const skipButton = this.canSkip ? `<button id="skip">skip</button>`  : '';
    return (
      `
      <div class="View">
        <div class="Step ${this.props.key}">
          <h1 class="Step__heading">${this.props.heading}</h1>
          ${templates}
          <button id="button">Submit</button>
          ${skipButton} 
          <p id="error" class="Step__error"></p>
          <p id="message" class="Step__message"></p>
        </div>
        </div>
      `
    )
  }
}
