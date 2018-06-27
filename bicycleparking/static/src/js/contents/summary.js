import Content from './content';
import questions from '../survey-questions';
import StateSession from '../state-session';

export default class Summary extends Content {
    constructor(survey) {
        super(...arguments);
        this.questions = questions;
    }

    get valid() {
        return this.values.length > 0;
    }

    get value() {
        return this.location;
    }

    bind(state) {
        var state = StateSession.getInstance().get();
        var questions = this.questions;
        var problems = state.problem_type.reduce((memo, value) => {
            memo += '<li><em>' + questions[0].questions[0].values.find(entry => entry.key === value).text + '</em></li>'
            return memo;
        }, '');
        document.getElementById('problems').innerHTML = problems;
        document.getElementById('date').innerHTML = new Date(state.happening[0].date).toLocaleString('en-US', { month: 'long', day: 'numeric' })
        document.getElementById('clock').innerHTML = new Date(state.happening[0].date).toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
        fetch(`${document.location.origin}/api/intersection`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'latitude': state.map[0][0], 'longitude': state.map[0][1] }),
        }).then(response => {
            response.json().then(json => {
                document.getElementById('intersection').innerHTML = json.major;
            })
        })
    }

    get template() {
        var problems = this.problems;
        return (`
        <div class="screen1 visible">
        <div class="progLine"><div class="progress prog5"></div></div>
        <h1>${this.props.heading}</h1>
            <div class="summary">
              <h2>Problems</h2>
              <div class="options summaryProblem"><div id="problems">
              </div></div>
              <div class="linebreak"></div>
              <h2> <em>Intersection </em> </h2>
              <div class="options summaryChange">
                  <li><em id="intersection"></em></li>
              </div>
                <div class="linebreak"></div>
              <h2>Date and time</h2>
              <div class="options third12">
                  <li><em id="date"></em></li>
              </div>
              <div class="options third3">
                  <li><em id="clock"></em></li>
              </div>
              <div class="linebreak"></div>
             <div>
                <div class="options half1 summaryChange noPhoto">
                     <li><em>Photo</em></li>
                    <div id="checkPhoto" class="check"></div>
                   </div>

              </div>
          </div>
      </div>
    </div>

      `
        )
    }
}