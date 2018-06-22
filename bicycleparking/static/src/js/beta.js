import StateSession from './state-session';

export default class Beta {
    constructor(index) {
        this.router = index.router;
    }


    render() {
        this.el = this.el || document.getElementById('render');
        this.el.innerHTML = this.template();
        this.bind();
    }

    submit() {
        var comment = { "comment": document.getElementsByClassName('comments')[0].value }
        fetch(`${document.location.origin}/api/comments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(comment),
        }).then(_ => {
            var state = StateSession.getInstance().get();
            state.finish = true;
            var state = StateSession.getInstance().save(state);
            this.router.navigate(`/home`)
        }).catch(_ => {
            var state = StateSession.getInstance().get();
            state.finish = true;
            var state = StateSession.getInstance().save(state);
            this.router.navigate(`/home`)
        });
    }
    bind() {
        document.getElementById('submitBetaComment').addEventListener('click', (event) => {
            this.submit();
        });
    }

    template() {
        return (`
        <header class="report">
        <div class="title"></div>
        <h2 class="betaBeaker">beta</h2>
      </header>  
      <div id="error" class="hidden"></div>   
    <div class="screen1 visible">
          <div class="progLine hidden"><div class="progress prog1"></div></div>
          <h1>Beta Tester Comments</h1>
          <textarea class="comments" rows="20" placeholder="You can write your comment here."></textarea>
        </div>   
      </div>
      <footer>
        <div class="nav">
                <div class="button">
                    <a id="submitBetaComment"><p><em>Send your comment</em></p></a>
                </div>
            </div>
        </footer> 
      `
        )
    }
}