
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
    document.getElementById('start').addEventListener('click', (event) => {
      this.survey.router.navigate(`/survey/1`);
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