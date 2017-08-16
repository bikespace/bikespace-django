import Step from '../step';

export default class Complete extends Step {
  get html() {
    const head = this.template(this.copy)
    const body = `<input type="email" id="email"><br><button id="button">Done</button>`;
    return `<div class="View View--light" />${head + body}</div>`;
  }

  bind() {
    document.getElementById('button').addEventListener('click', (event) => {
      const value = document.getElementById('email').value;
      this.survey.setState({
        email: value
      });
      //console.log(JSON.stringify(this.survey.state));
      var myHeaders = new Headers();
      var myInit = { method: 'GET',
               headers: myHeaders,
               mode: 'no-cors',//I am using no-cors because the request is going to a different url
               cache: 'default' };
      //I'm pretty sure this is sufficient
      fetch("http://example.com/",myInit).then(function(response) {
        console.log(response.json());
      }).then(function(data) {
        console.log(data);
      }).catch(function() {
        console.log("Booo");
      });
    });
  }
}
