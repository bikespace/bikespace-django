import Content from './content';

export default class Summary extends Content {
  constructor() {
    super(...arguments);
    this.values = [];
  }

  get valid() {
    return this.values.length > 0;
  }

  get value() {
    return this.values;
  }

  get template() {
    return (`
      <div class="screen1">
        <div class="progress prog5"></div>
        <h1>${this.props.heading}</h1>
        <div class="summary">
          <h1 class="titleSummary">Problems</h1>
          <div class="options">
              <li><em>dqsdqsdsqdsqdqsdqsdsqdqsdq</em></li>
          </div>
          <h1 class="titleSummary">Date & Time</h1>
          <div class="options">
              <li><em>January 25, 2018 at 3:30 PM</em></li>
          </div>
          <div>
            <div class="mapSummary">
              <h1 class="titleSummary">Location</h1>
            </div>            
            <div class="pictureSummary">
              <h1 class="titleSummary">Photo</h1>
            </div>
          </div>
        </div>        
      </div>
      `
    )
  }
}