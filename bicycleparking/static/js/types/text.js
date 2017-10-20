import Input from './input';

export default class TextInput extends Input {
  get template() {
    return (`
      <div class="input-field col">
        <textarea id="input" name="${this.props.key}" class="materialize-textarea"></textarea>
        <label for="${this.props.key}">${this.props.text}</label>
      </div>
      `
    )
  }
}