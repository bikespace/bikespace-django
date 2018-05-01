
export default class Beta {
    constructor(index) {
        this.router = index.router;
        this.state = localStorage.getItem('survey_state') ? JSON.parse(localStorage.getItem('survey_state')) : {};
    }


    render() {
        this.el = this.el || document.getElementById('render');
        this.el.innerHTML = this.template();
        this.bind();
    }

    submit() {
        var comment = { "comment": document.getElementsByClassName('comments')[0].value }
        console.log(comment);
        fetch(`${document.location.origin}/api/comments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(comment),
        }).then(_ => {
            this.state.finish = true;
            localStorage.setItem('survey_state',JSON.stringify(this.state));
            this.router.navigate(`/home`)
        }).catch(_ => {
            this.state.finish = true;
            localStorage.setItem('survey_state',JSON.stringify(this.state));
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
        <div class="title">
        </div>
    </header>    
    <div class="screen1 visible">
          <div class="progress prog5"></div>
          <h1>Beta Tester Comments :</h1>
          <textarea class="comments" rows="20" placeholder="You can write your comment here."></textarea>
        </div>   
      </div>
      <footer>
        <div class="nav">
                <div class="button bshadow">
                    <a id="submitBetaComment"><p><em>Send your comment</em></p></a>
                </div>
            </div>
        </footer> 
      `
        )
    }
}