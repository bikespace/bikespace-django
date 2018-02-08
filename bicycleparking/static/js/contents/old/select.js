import Input from './input';

export default class Select extends Input {
  constructor() {
    super(...arguments);
    this.selected = null;
  }

  get value() {
    return this.selected;
  }

  onSelect(event) {
    this.selected = event.target.value;
  }

  bind() {
    [...document.querySelectorAll(`input[name=${this.props.key}]`)].forEach(el => {
      el.onchange = this.onSelect.bind(this);
    })
  }

  get template() {
    const options = this.props.values.reduce((memo, value) => {
      memo += `<p> <input id="${value.key}" name="${this.props.key}" type="radio" value="${value.key}" /><label class="checkbox" for="${value.key}">${value.text}</label></p>`;
      return memo;
    }, '');
    const heading = this.props.heading ? `<h4>${this.props.heading}</h4>` : '';
    return (`
      <div className="question">
        ${heading}
        ${options}
      </div>
      `
    )
  }
}