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
    [...document.querySelectorAll('input')].forEach(el => {
      el.onchange = this.onSelect.bind(this);
    })
  }

  get template() {
    const options = this.props.values.reduce((memo, value) => {
      memo += `<p><label><input name="string-select" type="radio" value="${value.key}" name="problem" />${value.text}</label></p>`;
      return memo;
    }, '');
    return (`
      <div className="question">
        ${options}
      </div>
      `
    )
  }
}