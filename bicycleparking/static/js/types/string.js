import Input from './input';

export default class StringInput extends Input {
  get template() {
    const heading = this.props.heading ? `<h4>${this.props.heading}</h4>` : '';
    return (`
    <div class="input-field col">
      ${heading}
      <input name=${this.props.key}" id="${this.props.key}" type="text" class="validate">
      <label for="${this.props.key}">${this.props.text}</label>
    </div>
      `
    )
  }
}