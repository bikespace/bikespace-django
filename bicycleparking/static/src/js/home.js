import StateSession from './state-session';

export default class Home {
  constructor(survey) {
    this.survey = survey;
  }

  render() {
    this.el = this.el || document.getElementById('render');
    this.el.innerHTML = this.template();
    this.bind();
  }

  bind() {
    var state = StateSession.getInstance().get();
    if (state && state.finish) {
      document.getElementById('finish').classList.remove('hidden');
      StateSession.getInstance().destroy();
    }
    document.getElementById('start').addEventListener('click', (event) => {
      this.survey.router.navigate(`/start`);
    });
    let btnAdd=  document.getElementById('btnAdd')
    let deferredPrompt;

    window.addEventListener('beforeinstallprompt', (e) => {
      // Prevent Chrome 67 and earlier from automatically showing the prompt
      e.preventDefault();
      // Stash the event so it can be triggered later.
      deferredPrompt = e;
      btnAdd.style.display = 'block';
      console.log("hello")
    });

    btnAdd.addEventListener('click', (e) => {
    // hide our user interface that shows our A2HS button
    btnAdd.style.display = 'none';
    // Show the prompt
    deferredPrompt.prompt();
    // Wait for the user to respond to the prompt
    deferredPrompt.userChoice
      .then((choiceResult) => {
        if (choiceResult.outcome === 'accepted') {
          console.log('User accepted the A2HS prompt');
        } else {
          console.log('User dismissed the A2HS prompt');
        }
        deferredPrompt = null;
      });
  });
  }

  template() {
    return (
      `
      <header class="clear">
        <div class="title">
        </div>
      </header>
      <div id="start" class="screen1">
        <div id="finish" class="success hidden">
            <h1>Thank you</h1>
        </div>
          <div class="logo">
            <h1 class="maintitle tshadow">BikeSpace</h1>
          </div>
      
          <div class="nav">
                  <div class="button bshadow">
                      <a><p><em>Report a parking issue</em></p></a>
                  </div>
              </div>

          <div class="installPWA">
            <button id="btnAdd"></button>
          </div>
        </div>
      `
    )
  }
}