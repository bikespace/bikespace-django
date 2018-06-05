import Content from './content';

import flatpickr from "flatpickr";

export default class Happening extends Content {
  constructor() {
    super(...arguments);
    this.values = [];
  }

  get valid() {
    return this.values[0].time.length > 0;
  }

  get value() {
    this.values[0].date = new Date(
      this.flatpickrdate.latestSelectedDateObj.getFullYear(),
      this.flatpickrdate.latestSelectedDateObj.getMonth(),
      this.flatpickrdate.latestSelectedDateObj.getDate(),
      this.flatpickrtime.latestSelectedDateObj.getHours(),
      this.flatpickrtime.latestSelectedDateObj.getMinutes(),
      this.flatpickrtime.latestSelectedDateObj.getSeconds())
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
    this.values = this.getDataFromSession(this.props['key']);
    if (this.values.length == 0) {
      this.date = new Date();
      this.values.push({ 'date': this.date, 'time': [] });
    }
    var date = new Date(this.values[0].date);
    this.flatpickrdate = flatpickr("#date", {
      wrap: true, altInput: true,
      altFormat: "F j, Y",
      dateFormat: "Y-m-d", defaultDate: date,
    });
    this.flatpickrtime = flatpickr("#time", {
      wrap: true, enableTime: true,
      noCalendar: true,
      dateFormat: "h:i K", time_24hr: false, defaultDate: date
    });
    [...document.getElementsByClassName('check')].forEach(el => {
      el.addEventListener('click', this.onClick.bind(this));
    })

  }
  get template() {
    const options = this.props.values.reduce((memo, value) => {
      var cssClass = "check off"
      if (this.values.length > 0 && this.values[0].time) {
        if (this.values[0].time.includes(value.key)) {
          cssClass = "check on"
        }
      }
      memo += `<div class="options ${value.class}"><li><em>${value.text}</em></li><div class="${cssClass}" value="${value.key}"></div></div>`
      return memo;
    }, '');
    return (`
      <div class="screen1 visible">
        <div class="progLine"><div class="progress prog4"></div></div>
        <h1>${this.props.heading}</h1>
        <h2>${this.props.subtitle1}</h2>
    
        <ul>
            <div id=date>
                <div class="holder">
                    <input type="text" placeholder="Select Date.." data-input>
                    <div class="calendar" data-toggle></div>
                </div>
            </div>
                
            <div id=time>
                <div class="holder">
                    <input type="text" placeholder="Select Date.." data-input>
                    <div class="clock" data-toggle></div>
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