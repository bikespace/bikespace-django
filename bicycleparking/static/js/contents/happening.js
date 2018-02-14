import Content from './content';

export default class Happening extends Content {
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
    if (event.target.classList.contains("off")) {
      event.target.classList.replace("off", "on")
      this.values.push(event.target.getAttribute("value"));
    } else {
      event.target.classList.replace("on", "off")
      this.values.splice(this.values.indexOf(event.target.getAttribute("value")), 1);
    }
  }

  bind() {
    [...document.getElementsByClassName('check')].forEach(el => {
      el.addEventListener('click', this.onClick.bind(this));
    })
  }
  get template() {
    const options = this.props.values.reduce((memo, value) => {
      memo += `<div class="options"><li><em>${value.text}</em></li><div class="check off" value="${value.key}"></div></div>`
      return memo;
    }, '');
    return (`
      <div class="screen1">
        <div class="progress prog4"></div>
        <h1>${this.props.heading}</h1>
        <h2>${this.props.subtitle1}</h2>
        <ul>
              <div class="doubleoption">
                  <input id="deviceCamera" class="cameraButton" type="file" accept="image/*;capture=camera"/>
                  <div class="options">
                      <li><em>Camera</em></li>
                      <div class="check camera"> </div>
                  </div>                  
              </div>
              <div class="last"></div>
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