export default class Input {
  constructor(props, question) {
    this.props = props;
    this.submit = question.submit;
    this.onError = question.onError;
    this.onMessage = question.onMessage;
    this.router = question.router;
  }

  bind() {
    document.getElementById('button').addEventListener('click', (event) => {
      const value = document.getElementById('input').value;
      this.submit(value);
    });
    if (!this.props.required) {
      document.getElementById('skip').addEventListener('click', (event) => {
        this.submit(null);
      });
    }
  }
}
