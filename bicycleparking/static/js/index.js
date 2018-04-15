import Navigo from 'navigo';
import questions from './survey-questions';
import Home from './home';
import Beta from './beta';
import Survey from './survey';
class Index {
  constructor() {
    this.survey = {};
    this.router = new Navigo('/', true);
    this.survey = questions.map((question, i) => {
      let props = question;
      if (i + 1 === questions.length) {
        props = Object.assign({}, props, {
          final: true
        })
      }
      return new Survey(props, this)
    });
    this.home = new Home(this);
    this.beta = new Beta(this);
    try {
      this.state = localStorage.getItem('survey_state') ? JSON.parse(localStorage.getItem('survey_state')) : {};
    } catch (err) {
      this.state = {};
    }
    this.router.on({
      'survey/:pane': (params, query) => {
        this.renderPane(params, query)
      }, 'start': () => {
        this.renderStart();
      }, 'beta': () => {
        this.renderBeta();
      }, '*': () => {
        this.renderHome();
      }
    }).resolve();
  }

  back() {
    const back = parseInt(this.router.lastRouteResolved().params.pane, 10) - 1;
    if (back < 1) {
      this.router.navigate('/');
    } else {
      this.router.navigate(`/survey/${back}`)
    }
  }

  navigate() {
    const next = parseInt(this.router.lastRouteResolved().params.pane, 10) + 1;
    this.router.navigate(`/survey/${next}`)
  }

  submit() {
    console.log('submitting', this.state)

    // Marshall the state into API fields
    var body = {
      'latitude': this.state.map[0][0],
      'longitude': this.state.map[0][1],
      'survey': this.state
    };
    if (this.state.picture && this.state.picture.name) {

      fetch(`${document.location.origin}/api/upload/` + this.state.picture.name, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: this.state.picture,
      }).then(response => {
        response.json().then(json => {
          body.photo_uri = json.s3_name;
          fetch(`${document.location.origin}/api/survey`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
          }).then(_ => {
            this.router.navigate(`/beta`)
          }).catch(_ => {
            this.router.navigate(`/beta`)
          });
        });

      });
    } else {
      fetch(`${document.location.origin}/api/survey`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      }).then(_ => {
        this.router.navigate(`/beta`)
      }).catch(_ => {
        this.router.navigate(`/beta`)
      });
    }

  }

  setState(newState) {
    this.state = Object.assign({}, this.state, newState);
    localStorage.setItem('survey_state', JSON.stringify(this.state));
  }

  renderPane(params, query) {
    document.getElementById('render').classList.remove("image");
    let pane = parseInt(params.pane);
    this.survey[pane - 1].render();
  }

  renderStart(){
    this.survey.state= {}
    localStorage.removeItem('survey_state')
    this.router.navigate(`/survey/1`)
  }

  renderBeta() {
    this.beta.render();
  }
  renderHome() {
    this.home.render();
  }
}

new Index();
