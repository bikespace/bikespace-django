
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
      <div class="row center-sm center-md center-lg">
        <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
        </div>
        <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
            <object data="/static/images/BikeSpace_badge_black.svg" height="50%" width="100%" type="image/svg+xml"></object>      
        </div>
        <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
            <h1 class="title">Bike Parking</h1>
        </div>
        <div class="col-xs-12 col-sm-4 col-md-4 col-lg-4">
            <button id="start" class="btn lg">Let's get started</button>
        </div>       
      </div>
      `
    )
  }
}