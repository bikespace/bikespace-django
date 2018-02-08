import Content from './content';

export default class Picture extends Content {
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

  get template() {
    return (`
      <div class="screen1">
        <div class="progress prog2"></div>
        <h1>${this.props.heading}</h1>
        <h2>${this.props.text}</h2>
        <ul>
            <div class="doubleoption">
                <div class="options">
                    <li><em>test</em></li>
                    <div></div>
                    <input id="deviceCamera" class="cameraButton" type="file" accept="image/*;capture=camera">
                </div>
                <div class="options">
                    <li><em>test</em></li>
                    <div></div>
                    <input id="deviceInput" class="cameraButton" type="file" accept="image/*;capture=camera">
                </div>
            </div>
            <div class="last"></div>
        </ul>      
      </div>
      `
    )
  }
}