import StateSession from '../state-session';

export default class Content {
  constructor(props, question) {
    this.props = props;
    this.submit = question.submit;
    this.onError = question.onError;
    this.onMessage = question.onMessage;
    this.router = question.router;
  }

  getDataFromSession(name) {
    var instance = StateSession.getInstance().get()
    if (instance) {
      switch (name) {
        case "problem_type": return instance.problem_type ? instance.problem_type : []; return;
        case "picture": return instance.picture ? instance.picture : []; return;
        case "map": return instance.map ? instance.map : []; return;
        case "happening": return instance.happening ? instance.happening : []; return;   
        case "location": return instance.location ? instance.location : []; return;   
      }
    }
    return [];
  }
  get valid() {
    return !!this.value;
  }

  get value() {
    return document.getElementById(this.props.key).value;
  }

  bind() { }
}
