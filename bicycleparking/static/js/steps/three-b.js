import Step from '../step';

const options = [
  {
    value: 'short',
    text: '0-4 hours'
  },
  {
    value: 'med', 
    text: '4-8 hours'
  },
  {
    value: 'overnight',
    text: 'Overnight'
  },
  {
    value: 'longterm',
    text: 'Long-term'
  }
]

export default class StepThreeB extends Step {
  constructor() {
    super(...arguments);
    this.durations = [];
    console.log(this.survey.state)
  }
  
  onSelect(event) {
    if (event.target.checked) {
      this.durations.push(event.target.value);
    } else {
      this.durations.splice(this.durations.indexOf(event.target.value), 1);
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

  continue() {
    if (this.durations.length) {
      const durations = this.durations.reduce((memo, duration) => {
        memo[duration] = true;
        return memo;
      }, {})

      this.survey.setState({
        durations
      })
      this.router.navigate('/survey/4')
    }
  }
}