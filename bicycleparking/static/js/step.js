export default class Step {
  constructor(name, copy, survey) {
    this.name = name;
    this.survey = survey;
    this.router = survey.router;
    this.copy = copy;
    this.el = null;
    this.error = null;
    this.message = null;
  }

  template({name, title, heading, text}) {
    return (
      `
        <div class="Step ${name ? name : ""}">
          <h3 class="Step__title">${title}</p>
          <h1 class="Step__heading">${heading}</h1>
          <p class="Step__text">${text}</p>
          <p id="error" class="Step__error"></p>
          <p id="message" class="Step__message"></p>
        </div>
      `
    )
  }

  get html() {
    return this.template(this.copy)
  }

  render() {
    this.el = this.el || document.getElementById('render');
    this.el.innerHTML = this.html;
    this.el.className = '';
    this.el.classList.add(this.name)
    this.error = document.getElementById('error');
    this.message = document.getElementById('message');
    this.bind();
  }

  setMessage(text) {
    this.message = this.message || document.getElementById('message');
    this.message.textContent = text;
  }

  setError(text) {
    this.error = this.error || document.getElementById('error');
    this.error.textContent = text;
  }

  bind() {
  }
}
