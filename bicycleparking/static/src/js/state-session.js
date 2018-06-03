import State from "./state";


export default class StateSession {

  constructor() {
    var state = localStorage.getItem('state');
    if (!state) {
      state = new State();
      this.save(state);
    }
  }

  static getInstance() {
    if (!StateSession.instance) {
      this.instance = new StateSession();
    }
    return this.instance;
  }

  get() {
    return JSON.parse(localStorage.getItem('state'));
  }

  save(state) {
    localStorage.setItem('state', JSON.stringify(state))
  }

  destroy() {
    localStorage.removeItem('state');
    this.instance = null;
  }
}