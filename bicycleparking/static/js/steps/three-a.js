import Step from '../step';

function pad(val) {
  return val < 10 ? `0${val}` : val;
}

export default class StepThreeA extends Step {
  constructor() {
    super(...arguments);
  }

  get html() {
    const head = this.template(this.copy);
    const date = new Date();
    const month = pad(date.getMonth() + 1);
    const day = pad(date.getDate());
    const hour = pad(date.getHours());
    const minutes = pad(date.getMinutes());
    const dateString = `${date.getFullYear()}-${month}-${day}T${hour}:${minutes}`;
    const body = `<input type="datetime-local" id="date" /><br><button id="button">Done</button>`;
    return `<div class="View" />${head + body}</div>`;
  }

  bind() {
    document.getElementById('button').addEventListener('click', (event) => {
      const value = document.getElementById('date').value;
      this.survey.setState({
        timeFull: value
      });
      if (this.survey.state.issues && this.survey.state.issues.absent) {
        this.router.navigate('/survey/3b')
      } else {
        this.router.navigate('/survey/4')
      }
    });
  }
}
