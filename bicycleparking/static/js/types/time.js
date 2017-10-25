import Input from './input';

export default class TimeInput extends Input {

  constructor() {
    super(...arguments);    
  }
  
  bind() {
    $('.timepicker').pickatime({
      default: 'now', 
      fromnow: 0,     
      twelvehour: false,
      donetext: 'OK', 
      cleartext: 'Clear',
      canceltext: 'Cancel',
      autoclose: false,
      ampmclickable: true,
      aftershow: function(){} 
    });
  }
  get template() {
    return (`
        <div>
          <h3>${this.props.heading}</h3>
          <label for=${this.props.key}>Time</label>
          <input id="input" type="text" class="timepicker" name=${this.props.key}>
        </div>
      `
    )
  }
}