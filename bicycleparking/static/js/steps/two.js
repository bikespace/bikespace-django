import Step from '../step';

const options = [
  {
    value: 'full',
    text: 'All nearby bike racks were full'
  },
  {
    value: 'hidden',
    text: 'Difficult to locate bike racks'
  },
  {
    value: 'absent',
    text: 'No nearby bike racks'
  }
];

export default class StepTwo extends Step {
  constructor() {
    super(...arguments);
    this.problems = [];
  }

  onSelect(event) {
    if (event.target.checked) {
      this.problems.push(event.target.value);
    } else {
      this.problems.splice(this.problems.indexOf(event.target.value), 1);
    }
  }

  continue() {
    if (this.problems.length) {
      const problems = this.problems.reduce((memo, problem) => {
        memo[problem] = true;
        return memo;
      }, {})

      this.survey.setState({
        issues: problems
      })
      if (problems['full']) {
        this.router.navigate('/survey/3a')
      } else if (problems['absent']) {
        this.router.navigate('/survey/3b')
      } else {
        this.router.navigate('/survey/4')
      }
    }
  }

  bind() {
    [...this.el.querySelectorAll('input')].forEach(el => {
      el.onchange = this.onSelect.bind(this)
    });
    document.getElementById('button').addEventListener('click', this.continue.bind(this));
  }

  get html() {
    const head = this.template(this.copy)
    let choices = options.reduce((memo, option) => {
      memo += `<p><label><input type="checkbox" value="${option.value}" name="problem" />${option.text}</label></p>`
      return memo;
    }, '');
    choices = `<div class="choices">${choices}</div><button id="button">Done</button>`;
    return `<div class="View" />${head + choices}</div>`;
  }
}