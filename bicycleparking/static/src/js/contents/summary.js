import Content from './content';
import questions from '../survey-questions';

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
        this.state = state;
        var questions = this.questions;
        var problems = this.state.problem_type.reduce((memo, value) => {
            memo += '<div class="options"><li><em>' + questions[0].questions[0].values.find(entry => entry.key === value).text + '</em></li></div>'
            return memo;
        }, '');
        document.getElementById('problems').innerHTML = problems;
        document.getElementById('date').innerHTML = new Date(this.state.happening[0].date).toLocaleString('en-US', { month: 'long', day: 'numeric' })
        document.getElementById('clock').innerHTML = new Date(this.state.happening[0].date).toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
        if(this.state.picture){            
            document.getElementById('checkPhoto').classList.remove("off");
            document.getElementById('checkPhoto').classList.add("on");
        }else{
            document.getElementById('checkPhoto').classList.remove("on");
            document.getElementById('checkPhoto').classList.add("off");
        }
        if(this.state.map){
            document.getElementById('checkMap').classList.remove("off");
            document.getElementById('checkMap').classList.add("on");
        }else{
            document.getElementById('checkMap').classList.remove("on");
            document.getElementById('checkMap').classList.add("off");
        }
    }

    get template() {
        var problems = this.problems;
        return (`
    <div class="screen1 visible">
          <div class="progress prog5"></div>
          <h1>${this.props.heading}</h1>
                      <div class="summary">
                <h2>Problems</h2>
                <div id="problems">                
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
                    <div class="options half1">
                        <li><em>Photo</em></li>
                        <div id="checkPhoto" class="check"></div>
                    </div>
                    <div class="options half2">
                        <li><em>Location</em></li>
                        <div id="checkMap" class="check"></div>
                    </div>
                </div>
            </div>        
        </div>   
      </div>
      `
        )
    }
}