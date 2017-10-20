import Input from './input';

export default class TimeInput extends Input {

  constructor() {
    super(...arguments);    
    this.values="";
  }

  get value() {
    return this.values;
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
        <input type="text" class="timepicker" name=${this.props.key}>
      `
    )
  }
}