
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
      <div class="View">
        <div class="Step home">
          <h1 class="Step__heading">Bike Parking</h1>
          <p class="Step__text">Start Now</p>
          <button id="button">Start Now</button>
        </div>
      </div>
      `
    )
  }
}