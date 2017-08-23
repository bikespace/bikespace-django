function pad(val) {
  return val < 10 ? `0${val}` : val;
}

class Input {
  constructor(props, submit) {
    this.props = props;
    this.submit = submit;
  }
  
  bind() {
    document.getElementById('button').addEventListener('click', (event) => {
      const value = document.getElementById('input').value;
      this.submit(value);
    });
    if (!this.props.required) {
      document.getElementById('skip').addEventListener('click', (event) => {
        this.submit(null);
      });
    }
  }

}

class TextInput extends Input {
  get template() {
    const skipButton = this.props.required ? '' : `<button id="skip">skip</button>`;
    return (`
      <div className="question">
        <textarea name=${this.props.key} id="input"></textarea>
        <button id="button">Submit</button>
        ${skipButton}
      </div>
      `
    )
  }
}

class StringInput extends Input {
  get template() {
    const skipButton = this.props.required ? '' : `<button id="skip">skip</button>`;
    return (`
      <div className="question">
        <input type="text" name=${this.props.key} id="input" />
        <button id="button">Submit</button>
        ${skipButton}
      </div>
      `
    )
  }
}

class DateTimeInput extends Input {
  get template() {
    const date = new Date();
    const month = pad(date.getMonth() + 1);
    const day = pad(date.getDate());
    const hour = pad(date.getHours());
    const minutes = pad(date.getMinutes());
    const dateString = `${date.getFullYear()}-${month}-${day}T${hour}:${minutes}`;
    const skipButton = this.props.required ? '' : `<button id="skip">skip</button>`;
    return (`
      <div className="question">
        <input type="datetime-local" value="${dateString}" name=${this.props.key} id="input" />
        <button id="button">Submit</button>
        ${skipButton}
      </div>
      `
    )
  }
}

export default class Question {
  constructor(props, survey) {
    this.props = props;
    this.survey = survey;
    if (this.props.type === 'DATETIME') {
      this.input = new DateTimeInput(props, this.submit.bind(this))
    } else if (this.props.type === 'TEXT') {
      this.input = new TextInput(props, this.submit.bind(this))
    } else {
      this.input = new StringInput(props, this.submit.bind(this))
    }
  }

  submit(value) {
    if (value) {
      this.survey.setState({
        [this.props.key]: value
      })
      this.survey.navigate()
    } else {
      if (this.props.required) {
        console.log('error');
      } else {
        this.survey.navigate()
      }
    }
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