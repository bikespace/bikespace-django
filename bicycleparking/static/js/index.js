import Navigo from 'navigo';
import copy from './copy';
import Splash from './steps/splash';
import StepOneA from './steps/one-a';
import StepOneB from './steps/one-b';
import StepTwo from './steps/two';
import StepThreeA from './steps/three-a';
import StepThreeB from './steps/three-b';
import StepFour from './steps/four';
import Complete from './steps/complete';
import Step from './step';
import questions from './survey-questions';
import Question from './question';
import '../css/app.css';

class Survey {
  constructor() {
    this.steps = {};
    this.router = new Navigo('/', true);
    this.steps = questions.map((question) => {
      return new Question(question, this)
    })
    try {
      this.state = localStorage.getItem('survey_state') ? JSON.parse(localStorage.getItem('survey_state')) : {};
    } catch (err) {
      this.state = {};
    }
    this.router.on({
      'survey/:step': (params, query) => {
        this.renderStep(params, query)
      },
    }).resolve();
  }

  navigate() {
    const next = parseInt(this.router.lastRouteResolved().params.step, 10) + 1;
    this.router.navigate(`/survey/${next}`)
  }

  setState(newState) {
    this.state = Object.assign({}, this.state, newState);
    localStorage.setItem('survey_state', JSON.stringify(this.state));
  }

  renderStep(params, query) {
    let step = params.step;
    this.steps[step].render();
  }
}

new Survey();
