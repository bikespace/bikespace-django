import Input from './input';

export default class TextInput extends Input {
  get template() {
    const skipButton = this.props.required ? '' : `<button id="skip">skip</button>`;
    return (`
      <div className="question">
        <textarea name=${this.props.key} id="input"></textarea>
        <button id="button">Submit</button>
        ${skipButton}
      </div>
      `
    )
  }
}