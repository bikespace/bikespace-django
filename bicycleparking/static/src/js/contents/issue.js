import Content from './content';

export default class Issue extends Content {
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

  onClick(event) {
    var id;
    if (!event.target.getAttribute("value")) {
      id = event.target.parentElement.getAttribute("value");
    } else {
      id = event.target.getAttribute("value");
    }
    var check = document.getElementById(id);
    if (check.classList.contains("off")) {
      check.classList.replace("off", "on")
      this.values.push(id);
    } else {
      check.classList.replace("on", "off")
      this.values.splice(this.values.indexOf(id), 1);
    }
  }

  bind() {
    this.values = this.getDataFromSession(this.props['key']);
    [...document.getElementsByClassName('options')].forEach(el => {
      el.addEventListener('click', this.onClick.bind(this));
      if (this.values.filter(value => value === el.getAttribute("value")).length > 0) {
        document.getElementById(el.getAttribute("value")).classList.remove("off");
        document.getElementById(el.getAttribute("value")).classList.add("on");
      }
    });
  }

  get template() {
    const skipButton = this.props.required ? '' : `<button id="skip">skip</button>`;
    const options = this.props.values.reduce((memo, value) => {
      memo += `<div class="options" value="${value.key}"><li value="${value.key}"><em value="${value.key}">${value.text}</em></li><div id="${value.key}" class="check off" value="${value.key}"></div></div>`
      return memo;
    }, '');
    return (`
      <div class="screen1 visible">
        <div class="progLine"><div class="progress prog1"></div></div>
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