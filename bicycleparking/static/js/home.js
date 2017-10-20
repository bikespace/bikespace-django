
export default class Home {
  constructor(survey) {
    this.survey = survey;
  }

  render() {
    this.el = this.el || document.getElementById('render');
    this.el.innerHTML = this.template();
    this.bind();
  }

  bind() {
    document.getElementById('button').addEventListener('click', (event) => {
      this.survey.router.navigate(`/survey/1`);
    });
  }

  template() {
    return (
      `
      <h1 class="title">Bike Parking</h1>
      <h2 class="subtitle is-1">Start Now</h2>
      
      <button id="button" class="waves-effect waves-light btn">Start Now</button>
      `
    )
  }
}