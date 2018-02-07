import TextInput from './types/text';
import StringInput from './types/string';
import DateTimeInput from './types/date';
import TimeInput from './types/time';
import MapInput from './types/map';
import ArrayInput from './types/array';
import SelectInput from './types/select';
import ImageInput from './types/image';
import types from './types/types';

const formatKey = (key) => {
  return key.split('_').map(string => string.charAt(0).toUpperCase() + string.slice(1)).join(' ');
}

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
    }if (props.type === types.TIME) {
      return new TimeInput(props, question)
    } else if (props.type === types.TEXT) {
      return new TextInput(props, question);
    } else if (props.type === types.MAP) {
      return new MapInput(props, question);
    } else if (props.type === types.ARRAY) {
      return new ArrayInput(props, question);
    } else if (props.type === types.IMAGE) {
      return new ImageInput(props, question);
    } else if (props.type === types.STRING && props.values && props.values.length) {
      return new SelectInput(props, question);
    } else {
      return new StringInput(props, question);
    }
  }

  get errors() {
    return this.questions.reduce((memo, question) => {
      if (question.props.required && !question.valid) {
        memo = memo.concat([question])
      }
      return memo;
    }, []);
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
    } else if (this.errors.length) {
      this.error.innerHTML = this.errors.reduce((memo, err) => {
        return memo += `Field <em>${formatKey(err.props.key)}</em> is required. <br>`
      }, '');
    } else {
      this.survey.navigate()
    }
  }

  onError(error) {
    this.error.textContent = error;
  }

  onMessage(message) {
    this.message.textContent = message;
  }

  render() {
    this.el = this.el || document.getElementById('render');
    this.el.innerHTML = this.template();
    this.el.classList.add(this.props.key)
    this.error = document.getElementById('error');
    this.message = document.getElementById('message');
    this.bind();
  }

  bind() {
    document.getElementById('button').addEventListener('click', (event) => {
      this.submit();
    });

    this.questions.forEach((question) => {
      question.bind();
    })
  }

  template() {
    const templates = this.questions.reduce((memo, question) => {
      memo += question.template;
      return memo;
    }, '')
    const buttonText = this.props.final ? 'Submit' : 'Next';
    const heading = this.props.heading ? `<h3>${this.props.heading}</h3>` : '';
    return (
      `
      <header class="report">
          <div class="title">
          </div>
      </header>
        ${templates}
        <footer>
            <div class="nav">
                <div class="back">
                    <a href="index.html">
                        <p>
                            <em>Back</em>
                        </p>
                    </a>
                </div>
                <div class="next">
                    <a id="button">
                        <p>
                            <em>Next</em>
                        </p>
                    </a>
                </div>
            </div>
        </footer>   
      `
    )
  }
}
