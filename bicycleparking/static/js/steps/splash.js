import Step from '../step';

export default class Splash extends Step {
  get html() {
    const head = this.template(this.copy);
    const body = 
      `<div class="Splash" />
        <button type="button" id="button" class="button Splash__button">
          Begin
        </button>
      </div>`;
    return `<div class="View" />${head + body}</div>`;
  }

  bind() {
    document.getElementById('button').addEventListener('click', (evt) => {
      this.router.navigate('/survey/1a')
    })
  }
}
