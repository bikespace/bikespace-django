import Input from './input';
import flatpickr from 'flatpickr';

export default class DateTimeInput extends Input {

  constructor() {
    super(...arguments);
  }

  bind() {
    flatpickr(`#${this.props.key}`, {
      enableTime: true,
    })
  }

  get template() {
    const heading = this.props.heading ? `<h4>${this.props.heading}</h4>` : '';
    return (`
      <div>
        ${heading}
        <label for=${this.props.key}>Date</label>
        <input id="${this.props.key}" type="text" class="datepicker" name=${this.props.key}>
      </div>
      `
    )
  }
}