import Input from './input';

function pad(val) {
  return val < 10 ? `0${val}` : val;
}

export default class DateTimeInput extends Input {
  get template() {
    const date = new Date();
    const month = pad(date.getMonth() + 1);
    const day = pad(date.getDate());
    const hour = pad(date.getHours());
    const minutes = pad(date.getMinutes());
    const dateString = `${date.getFullYear()}-${month}-${day}T${hour}:${minutes}`;
    return (`
      <div className="question">
        <label class="Step__text">${this.props.text}</label>
        <input type="datetime-local" value="${dateString}" name=${this.props.key} id="input" />
      </div>
      `
    )
  }
}