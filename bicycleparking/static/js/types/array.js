import Input from './input';

export default class ArrayInput extends Input {
  constructor() {
    super(...arguments);
    this.values = [];
  }

  get valid() {
    return this.values.length > 0;
  }

  get value() {
    return this.values;
  }

  onSelect(event) {
    if (event.target.type === 'checkbox') {
      if (event.target.checked) {
        this.values.push(event.target.value);
      } else {
        this.values.splice(this.values.indexOf(event.target.value), 1);
      }
    }
  }

  bind() {
    [...document.querySelectorAll('input')].forEach(el => {
      el.onchange = this.onSelect.bind(this);
    })
  }

  get template() {
    const skipButton = this.props.required ? '' : `<button id="skip">skip</button>`;
    const options = this.props.values.reduce((memo, value) => {
      memo += `<p><input type="checkbox"  id="${value.key}" value="${value.key}" name="problem" /><label for="${value.key}">${value.text}</label></p>`
      return memo;
    }, '');
    const heading = this.props.heading ? `<h4>${this.props.heading}</h4>` : '';
    return (`
      <div className="question">
        ${heading}
        <p>${this.props.text}</p>
        ${options}
      </div>
      `
    )
  }
}