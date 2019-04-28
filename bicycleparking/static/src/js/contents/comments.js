import Content from './content';

export default class Comments extends Content {
  constructor() {
    super(...arguments);
    this.values = [];
  }

  get valid() {
    return this.values.length > 0;
  }

  get value() {
    return document.getElementById('text_comment').value;
  }

 
  bind() {
    this.values = this.getDataFromSession(this.props['key']);
    if(this.values.length > 0){
      document.getElementById('text_comment').value = this.values;
    }
    
  }

  get template() {
    return (`
        <div class="screen1 visible">
            <div class="progLine"><div class="progress prog5"></div></div>
            <h1>${this.props.heading}</h1>
            <h2>${this.props.text}</h2>
            <textarea id="text_comment" class="comments" rows="20" placeholder="You can write your comment here."></textarea>
        </div>
      `
    )
  }
}