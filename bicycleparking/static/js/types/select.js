import Input from './input';

export default class Select extends Input {
  constructor() {
    super(...arguments);
    this.value = null;
  }

  onSelect(event) {
    this.value = event.target.value;
  }

  bind() {
    document.getElementById('button').addEventListener('click', (event) => {
      this.submit(this.value);
    });
    [...document.querySelectorAll('input')].forEach(el => {
      el.onchange = this.onSelect.bind(this);
    })
  }

  get template() {
    const skipButton = this.props.required ? '' : `<button id="skip">skip</button>`;
    const options = this.props.values.reduce((memo, value) => {
      memo += `<p><label><input name="string-select" type="radio" value="${value.key}" name="problem" />${value.text}</label></p>`;
      return memo;
    }, '');
    return (`
      <div className="question">
        ${options}
        <button id="button">Submit</button>
        ${skipButton}
      </div>
      `
    )
  }
}