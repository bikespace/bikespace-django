const types = {
  LATLNG: 'LATLNG',
  STRING: 'STRING',
  TEXT: 'TEXT',
  NUMBER: 'NUMBER',
  ARRAY: 'ARRAY',
  DATETIME: 'DATETIME',
  IMAGRE: 'IMAGE'
}

const questions = [
  {
    key: 'target_location',
    type: types.LATLNG,
    heading: 'Where were you trying to go?',
    text: 'Tell us where you were trying to go or where you tried to park',
    required: true
  },
  {
    key: 'problem_type',
    type: types.ARRAY,
    heading: 'What was the problem here?',
    text: 'select all that apply',
    required: true,
    values: [
      {
        key: 'full',
        text: 'All nearby bike racks were full'
      },
      {
        key: 'difficult',
        text: 'Difficult to locate bike racks'
      },
      {
        key: 'absent',
        text: 'No nearby bike racks'
      }
    ]
  },
  {
    key: 'report_time',
    type: types.DATETIME,
    required: true,
    heading: 'When did you identify the problem?',
    text: 'Specify the time and date',
    default: new Date() 
  },
  {
    key: 'duration',
    type: types.STRING,
    heading: 'How long were you planning to lock your bike?',
    required: true,
    text: '',
    values: [
      {
        key: 'short',
        text: 'Less than 1 hour'
      },
      {
        key: 'med',
        text: 'Up to 8 hours'
      },
      {
        key: 'long',
        text: 'Overnight'
      }
    ]
  },
  {
    key: 'comment',
    type: types.TEXT,
    heading: 'Anything else?',
    text: 'Please leave a short comment',
  },
  {
    key: 'photo',
    type: types.IMAGE,
    heading: 'Upload a picture',
    text: 'Optionally upload an image of a problem'
  },
  {
    key: 'email',
    type: types.STRING,
    heading: 'Let\'s keep in touch',
    text: 'Sign up to receive updates'
  }
]

export default questions;