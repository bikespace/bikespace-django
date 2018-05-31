
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
    this.state = localStorage.getItem('survey_state') ? JSON.parse(localStorage.getItem('survey_state')) : {};
    if (this.state && this.state.finish) {
      document.getElementById('finish').classList.remove('hidden');
    }
    document.getElementById('start').addEventListener('click', (event) => {
      this.survey.router.navigate(`/start`);
    });
  }

  template() {
    return (
      `
      <header class="clear">
        <div class="title">
        </div>
      </header>
      <div class="screen1">
        <div id="finish" class="success hidden">
            <h1>Thank you</h1>
        </div>
          <div class="logo">
            <h1 class="maintitle tshadow">BikeSpace</h1>
          </div>
      </div>
      <footer>
          <div class="nav">
                  <div class="button bshadow">
                      <a id="start"><p><em>Report a parking issue</em></p></a>
                  </div>
              </div>
      </footer> 
      `
    )
  }
}