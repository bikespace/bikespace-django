import types from './types/types';

const questions = [
  {
    questions: [
      {
        key: 'problem_type',
        type: types.ARRAY,
        heading: 'What was the issue?',
        text: 'Choose what applies',
        required: true,
        error: 'Choose at least one option',
        values: [
          {
            key: 'absent',
            text: "Couldn't find bike parking"
          },
          {
            key: 'full',
            text: "Nearby bike parking is full"
          },
          {
            key: 'damaged',
            text: "Bike parking is damaged"
          },
          {
            key: 'badly',
            text: "A bike is badly parked"
          },
          {
            key: 'other',
            text: "Different problem"
          }
        ]
      }
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