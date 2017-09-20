import Input from './input';

export default class TextInput extends Input {
  get template() {
    return (`
      <div className="question">
        <textarea name=${this.props.key} id="input"></textarea>
      </div>
      `
    )
  }
}