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
import '../css/app.css';

const steps = {
  splash: Splash,
  '1a': StepOneA,
  '1b': StepOneB,
  '2': StepTwo,
  '3a': StepThreeA,
  '3b': StepThreeB,
  '4': StepFour,
  complete: Complete,
}

class Survey {
  constructor() {
    this.steps = {};
    this.router = new Navigo('/', true);
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
        this.renderHome()
      },
    }).resolve();
  }

  setState(newState) {
    this.state = Object.assign({}, this.state, newState);
    localStorage.setItem('survey_state', JSON.stringify(this.state));
  }

  renderHome() {
    this.steps.home = this.steps.home || new Splash('splash', copy.splash, this);
    this.steps.home.render();
  }

  renderStep(params, query) {
    let step = params.step;
    this.steps[step] = this.steps[step] || new steps[step](step, copy[step], this);
    this.steps[step].render();
  }
}

new Survey();
