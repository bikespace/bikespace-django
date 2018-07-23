import Issue from './contents/issue';
import Map from './contents/map';
import Happening from './contents/happening';
import Picture from './contents/picture';
import Comments from './contents/comments';
import Summary from './contents/summary';
import contents from './contents/contents';


export default class Survey {
  constructor(props, survey) {
    this.props = props;
    this.survey = survey;
    const question = {
      submit: this.submit.bind(this),
      onError: this.onError.bind(this),
      onMessage: this.onMessage.bind(this),
      router: this.survey.router
    }
    this.questions = this.props.questions.map((q) => {
      return this.createContent(q, question)
    });
  }

  createContent(props, question) {
    if (props.type === contents.ISSUES) {
      return new Issue(props, question);
    } else if (props.type === contents.MAP) {
      return new Map(props, question, this.survey);
    } else if (props.type === contents.HAPPENING) {
      return new Happening(props, question);
    } else if (props.type === contents.PICTURE) {
      return new Picture(props, question);
    } else if (props.type === contents.COMMENTS) {
      return new Comments(props, question);
    } else if (props.type === contents.SUMMARY) {
      return new Summary(props, question);
    }
  }

  get errors() {
    return this.questions.reduce((memo, question) => {
      if (question.props.required && !question.valid) {
        memo = memo.concat([question])
      }
      return memo;
    }, []);
  }


  submit() {
    const values = this.questions.reduce((memo, question) => {
      memo[question.props.key] = question.value;
      return memo;
    }, {})
    if (values) {
      this.survey.setState(values)
    }
    if (this.props.final) {
      this.survey.submit();
    } else if (this.errors.length) {
      this.error.innerHTML = this.errors.reduce((memo, err) => {
        return memo += '<h1>' + err.props.error + '</h1>';
      }, '');
      this.error.classList.remove("hidden");
    } else {
      this.survey.navigate()
    }
  }

  back() {
    this.survey.back()
  }

  onError(error) {
    this.error.textContent = error;
  }

  onMessage(message) {
    this.message.textContent = message;
  }

  render() {
    this.el = this.el || document.getElementById('render');
    this.el.innerHTML = this.template();
    this.el.classList.add(this.props.key)
    this.error = document.getElementById('error');
    this.error.classList.add("hidden");
    this.message = document.getElementById('message');

    this.bind();
  }

  bind() {
    const state = this.survey.state;
    document.getElementById('next').addEventListener('click', (event) => {
      this.submit();
    });

    document.getElementById('back').addEventListener('click', (event) => {
      this.back();
    });

    this.questions.forEach((question) => {
      question.bind(state);
    })
  }

  template() {
    const templates = this.questions.reduce((memo, question) => {
      memo += question.template;
      return memo;
    }, '')
    const buttonText = this.props.final ? 'Submit' : 'Next';
    const heading = this.props.heading ? `<h3>${this.props.heading}</h3>` : '';
    return (
      `
      <header class="report">
        <div class="title"></div>
      </header>  
      <div id="error" class="hidden red"></div>  
        ${templates}
        <footer>
            <div class="nav">
                <div class="back">
                    <a id="back">
                        <p>
                            <em>Back</em>
                        </p>
                    </a>
                </div>
                <div class="next">
                    <a id="next">
                        <p>
                            <em>${buttonText}</em>
                        </p>
                    </a>
                </div>
            </div>
        </footer>   
      `
    )
  }
}
