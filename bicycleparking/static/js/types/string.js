import Input from './input';

export default class StringInput extends Input {
  get template() {
    return (`
      <div className="question">
        <label class="Step__text">${this.props.text}</label>
        <input type="text" name=${this.props.key} id="input" />
      </div>
      `
    )
  }
}