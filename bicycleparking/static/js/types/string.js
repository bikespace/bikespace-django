import Input from './input';

export default class StringInput extends Input {
  get template() {
    return (`
    <div class="input-field col">
    <input name=${this.props.key}" id="input" type="text" class="validate">
    <label for="${this.props.key}">${this.props.text}</label>
  </div>
      `
    )
  }
}