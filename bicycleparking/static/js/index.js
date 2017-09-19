import Navigo from 'navigo';
import questions from './survey-questions';
import Home from './home';
import Question from './question';
import '../css/app.css';

class Survey {
  constructor() {
    this.steps = {};
    this.router = new Navigo('/', true);
    this.steps = questions.map((question, i) => {
      let props = question;
      if (i + 1 === questions.length) {
         props = Object.assign({}, props, {
           final: true
         })
      }
      return new Question(props, this)
    });
    this.home = new Home(this);
    try {
      this.state = localStorage.getItem('survey_state') ? JSON.parse(localStorage.getItem('survey_state')) : {};
    } catch (err) {
      this.state = {};
    }
    this.router.on({
      'survey/:step': (params, query) => {
        this.renderStep(params, query)
      },
      '*': () => {
        this.renderHome();
      }
    }).resolve();
  }

  navigate() {
    const next = parseInt(this.router.lastRouteResolved().params.step, 10) + 1;
    this.router.navigate(`/survey/${next}`)
  }

  submit() {
    console.log(this.state)

    // Marshall the state into API fields
    var body = {
      'latitude': this.state.target_location.lat,
      'longitude': this.state.target_location.lng,
      'comments': this.state.comment,
      'point_timestamp': this.state.report_time,
      'survey': this.state
    };

    fetch(`${document.location.origin}/api/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
  }

  setState(newState) {
    this.state = Object.assign({}, this.state, newState);
    localStorage.setItem('survey_state', JSON.stringify(this.state));
  }

  renderStep(params, query) {
    let step = parseInt(params.step);
    this.steps[step - 1].render();
  }

  renderHome() {
    this.home.render();
  }
}

new Survey();
