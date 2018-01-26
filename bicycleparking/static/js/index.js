import Navigo from 'navigo';
import questions from './survey-questions';
import Home from './home';
import Review from './review';
import Pane from './pane';
import '../css/app.css';
import '../css/leaflet.css';
import '../css/leaflet.mobile.css';

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
      }, 'review': (params, query) => {
        this.renderReview(params, query)
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
      'latitude': this.state.location.lat,
      'longitude': this.state.location.lng,
      'comments': this.state.comment,
      'survey': this.state
    };
    if (this.state.photo) {
      fetch(`${document.location.origin}/api/upload/` + this.state.photo.name, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: this.state.photo,
      }).then(response => {
        response.json().then(json => {
          body.photo_uri = json.s3_name;
          fetch(`${document.location.origin}/api/survey`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
          }).then(_ => { this.router.navigate(`/review`) });
        });

      });
    } else {
      fetch(`${document.location.origin}/api/survey`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      }).then(_ => { this.router.navigate(`/review`) });
    }

  }

  setState(newState) {
    this.state = Object.assign({}, this.state, newState);
    localStorage.setItem('survey_state', JSON.stringify(this.state));
  }

  renderPane(params, query) {
    document.getElementById('render').classList.remove("image");
    let pane = parseInt(params.pane);
    this.panes[pane - 1].render();
  }

  renderReview() {
    new Review(this).render();
  }

  renderHome() {
    this.home.render();
  }
}

new Survey();
