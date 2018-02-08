import Input from './input';

export default class TextInput extends Input {
  get template() {
    const heading = this.props.heading ? `<h4>${this.props.heading}</h4>` : '';
    return (`
      <div class="input-field col">
        ${heading}
        <textarea id="${this.props.key}" name="${this.props.key}" class="materialize-textarea"></textarea>
        <label for="${this.props.key}">${this.props.text}</label>
      </div>
      `
    )
  }
}