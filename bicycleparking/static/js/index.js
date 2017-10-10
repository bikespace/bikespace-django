import Navigo from 'navigo';
import questions from './survey-questions';
import Home from './home';
import Pane from './pane';
import '../css/app.css';

class Survey {
  constructor() {
    this.panes = {};
    this.router = new Navigo('/', true);
    this.panes = questions.map((question, i) => {
      let props = question;
      if (i + 1 === questions.length) {
         props = Object.assign({}, props, {
           final: true
         })
      }
      return new Pane(props, this)
    });
    this.home = new Home(this);
    try {
      this.state = localStorage.getItem('survey_state') ? JSON.parse(localStorage.getItem('survey_state')) : {};
    } catch (err) {
      this.state = {};
    }
    this.router.on({
      'survey/:pane': (params, query) => {
        this.renderPane(params, query)
      },
      '*': () => {
        this.renderHome();
      }
    }).resolve();
  }

  navigate() {
    const next = parseInt(this.router.lastRouteResolved().params.pane, 10) + 1;
    this.router.navigate(`/survey/${next}`)
  }

  submit() {
    console.log('submitting', this.state)

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

  renderPane(params, query) {
    let pane = parseInt(params.pane);
    this.panes[pane - 1].render();
  }

  renderHome() {
    this.home.render();
  }
}

new Survey();
