import Input from './input';

export default class StringInput extends Input {
  get template() {
    const skipButton = this.props.required ? '' : `<button id="skip">skip</button>`;
    return (`
      <div className="question">
        <input type="text" name=${this.props.key} id="input" />
        <button id="button">Submit</button>
        ${skipButton}
      </div>
      `
    )
  }
}