import Navigo from 'navigo';
import questions from './survey-questions';
import Home from './home';
import Survey from './survey';
import StateSession from './state-session';

class Index {

  constructor() {
    this.survey = {};
    StateSession.getInstance().destroy();
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
    this.router.on({
      'survey/:pane': (params, query) => {
        this.renderPane(params, query)
      }, 'start': () => {
        this.renderStart();
      }, '*': () => {
        this.renderHome();
      }
    }).resolve();
  }

  locationAcquired(position) {
    localStorage.setItem('my_localisation', JSON.stringify({ lat: position.coords.latitude, lng: position.coords.longitude }));
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
    var state = StateSession.getInstance().get();

    // Marshall the state into API fields
    var body = {
      'latitude': state.map[0][0],
      'longitude': state.map[0][1],
      'survey': state
    };
    if (state.picture) {
      fetch(`${document.location.origin}/api/upload/pictures`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'picture': state.picture }),
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
            var state = StateSession.getInstance().get();
            state.finish = true;
            var state = StateSession.getInstance().save(state);
            this.router.navigate(`/home`)
          }).catch(_ => {
            var state = StateSession.getInstance().get();
            state.finish = true;
            var state = StateSession.getInstance().save(state);
            this.router.navigate(`/home`)
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
        var state = StateSession.getInstance().get();
        state.finish = true;
        var state = StateSession.getInstance().save(state);
        this.router.navigate(`/home`)
      }).catch(_ => {
        var state = StateSession.getInstance().get();
        state.finish = true;
        var state = StateSession.getInstance().save(state);
        this.router.navigate(`/home`)
      });
    }

  }

  setState(newState) {
    var state = Object.assign({}, StateSession.getInstance().get(), newState);
    StateSession.getInstance().save(state);
  }


  renderPane(params, query) {
    document.getElementById('render').classList.remove("image");
    let pane = parseInt(params.pane);
    this.survey[pane - 1].render();
  }

  renderStart() {
    this.router.navigate(`/survey/1`)
  }
  renderHome() {
    if ('geolocation' in navigator) {
      this.watchId = navigator.geolocation.watchPosition(this.locationAcquired);
    }
    this.home.render();
  }
}

new Index();
