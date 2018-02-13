import contents from './contents/contents';

const questions = [
  {
    questions: [
      {
        key: 'problem_type',
        type: contents.ISSUES,
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
    questions: [
      {
        key: 'picture',
        type: contents.PICTURE,
        heading: 'Add a photo',
        text: 'Optional',
        error: 'Picture is required',
        required: true,
      }
    ]
  }, {
    questions: [
      {
        key: 'map',
        type: contents.MAP,
        heading: 'Where was the problem ?',
        text: 'Pin the location',
        required: false,
      }
    ]
  }, {
    questions: [
      {
        key: 'happening',
        type: contents.HAPPENING,
        heading: 'When did this happen ?',
        text: 'Specify the date and time',
        required: true,
        values: [
          {
            key: 'minutes',
            text: "minutes"
          },
          {
            key: 'hours',
            text: "hours"
          },
          {
            key: 'overnight',
            text: "overnight"
          },
          {
            key: 'days',
            text: "days"
          }
        ]
      }
    ]
  }, {
    questions: [
      {
        key: 'summary',
        type: contents.SUMMARY,
        heading: 'Summary',
        required: false,
        final: true

      }
    ]
  },
]

export default questions;