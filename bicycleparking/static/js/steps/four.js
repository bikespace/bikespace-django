import Step from '../step';

export default class StepFour extends Step {
  get html() {
    const head = this.template(this.copy)
    const body = `<textarea id="comment"></textarea><br><button id="button">Done</button>`;
    return `<div class="View View--light" />${head + body}</div>`;
  }

  bind() {
    document.getElementById('button').addEventListener('click', (event) => {
      const value = document.getElementById('comment').value;
      this.survey.setState({
        comment: value
      });
      this.router.navigate('/survey/complete')
    });
  }
}