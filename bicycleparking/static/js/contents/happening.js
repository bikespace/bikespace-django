import Content from './content';
import flatpickr from 'flatpickr';

export default class Happening extends Content {
  constructor() {
    super(...arguments);
    this.values = [];
    this.date = new Date();
    this.values.push({ 'date': this.date, 'time': [] });
  }

  get valid() {
    return this.values[0].time.length > 0;
  }

  get value() {
    return this.values;
  }

  onClick(event) {
    if (event.target.classList.contains("off")) {
      event.target.classList.replace("off", "on")
      this.values[0].time.push(event.target.getAttribute("value"));
    } else {
      event.target.classList.replace("on", "off")
      this.values[0].time.splice(this.values.indexOf(event.target.getAttribute("value")), 1);
    }
  }

  bind() {
    flatpickr('#calendar', {
    });
    [...document.getElementsByClassName('check')].forEach(el => {
      el.addEventListener('click', this.onClick.bind(this));
    })
    document.getElementById('date').innerHTML = this.date.toLocaleString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
    document.getElementById('clock').innerHTML = this.date.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
  }
  get template() {
    const options = this.props.values.reduce((memo, value) => {

      memo += `<div class="options ${value.class}"><li><em>${value.text}</em></li><div class="check off" value="${value.key}"></div></div>`
      return memo;
    }, '');
    return (`
      <div class="screen1 visible">
        <div class="progress prog4"></div>
        <h1>${this.props.heading}</h1>
        <h2>${this.props.subtitle1}</h2>
    
        <ul>
            <div class="doubleoption">
              <input id="calendar" class="datepicker" type="text" name="calendar" />
                <div class="options">
                      <li><em id="date"></em></li>
                      <div class="check calendar"> </div>
                  </div>
                  <div class="options">
                      <li><em id="clock"></em></li>
                      <div class="check clock"> </div>
                  </div>
              </div>
          </ul> 
          <h2>${this.props.subtitle2}</h2>
        <ul>
          ${options}
        </ul>
      </div>
      `
    )
  }
}