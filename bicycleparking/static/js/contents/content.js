export default class Content {
  constructor(props, question) {
    this.props = props;
    this.submit = question.submit;
    this.onError = question.onError;
    this.onMessage = question.onMessage;
    this.router = question.router;
  }

  get valid() {
    return !!this.value;
  }
  
  get value() {
    return document.getElementById(this.props.key).value;
  }

  bind() {}
}
