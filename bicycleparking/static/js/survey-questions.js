import types from './types/types';

const questions = [
  {
    questions: [
      {
        key: 'problem_type',
        type: types.ARRAY,
        heading: 'What problem(s) prevented you from parking your bike?',
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
        key: 'photo',
        type: types.IMAGE,
        heading: 'Upload a picture',
        text: 'Optionally upload an image of a problem'
      },
    ]
  },
  {
    heading: 'Where were you going?',
    questions: [
      {
        key: 'location',
        type: types.MAP,
        text: 'Tell us where you were trying to go or where you tried to park',
        required: true
      },
    ]
  },
  {
    questions: [
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
    ]
  },
  {
    heading: 'Anything else?',
    questions: [{
      key: 'comment',
      type: types.TEXT,
      text: 'Please leave a short comment',
    },
    {
      key: 'email',
      type: types.STRING,
      text: 'Sign up to receive updates'
    }]
  }

]

export default questions;