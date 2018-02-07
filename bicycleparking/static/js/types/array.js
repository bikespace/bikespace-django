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
    if (event.target.type === 'div') {
      if (event.target.checked) {
        this.values.push(event.target.value);
      } else {
        this.values.splice(this.values.indexOf(event.target.value), 1);
      }
    }
  }

  bind() {
    [...document.querySelectorAll('options')].forEach(el => {
      el.addEventListener('click', function (event) {
        console.log("tatq");
      });
    })
  }


  get template() {
    const skipButton = this.props.required ? '' : `<button id="skip">skip</button>`;
    const options = this.props.values.reduce((memo, value) => {
      memo += `<div class="options"><li><em>${value.text}</em></li><div class="check off"></div></div>`
      return memo;
    }, '');
    return (`
      <div class="screen1">
        <h1>${this.props.heading}</h1>
        <h2>${this.props.text}</h2>
        <ul>
          ${options}
        </ul>
      </div>
      `
    )
  }
}