import Content from './content';

export default class Map extends Content {
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
        <div class="progress prog3"></div>
        <h1>${this.props.heading}</h1>
        <h2>${this.props.text}</h2>

      </div>
      `
    )
  }
}