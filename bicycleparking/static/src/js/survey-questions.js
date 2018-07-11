import contents from './contents/contents';

const questions = [
  {
    questions: [
      {
        key: 'problem_type',
        type: contents.ISSUES,
        heading: 'What was the issue?',
        text: 'Choose at least one',
        required: true,
        error: 'Choose an issue',
        values: [
          {
            key: 'absent',
            text: "Bike parking is <strong>not provided</strong>"
          },
          {
            key: 'full',
            text: "Bike parking is <strong>full</strong>"
          },
          {
            key: 'damaged',
            text: "Bike parking is <strong>damaged</strong>"
          },
          {
            key: 'badly',
            text: "A bike is <strong>abandoned</strong>"
          },
          {
            key: 'other',
            text: "Something else"
          }
        ]
      }
    ]
  }, {
    questions: [
      {
        key: 'map',
        type: contents.MAP,
        heading: 'Where was the problem?',
        text: 'Pin the location',
        required: false,
      }
    ]
  }, {
    questions: [
      {
        key: 'happening',
        type: contents.HAPPENING,
        heading: 'When did this happen?',
        subtitle1: 'Date',
        subtitle2 : 'How long did you need to park?',
        error: 'Choose an option',
        required: true,
        values: [
          {
            key: 'minutes',
            text: "minutes",
            class: 'half1'
          },
          {
            key: 'hours',
            text: "hours",
            class: 'half2'
          },
          {
            key: 'overnight',
            text: "overnight",
            class: 'half1'
          },
          {
            key: 'days',
            text: "days",
            class: 'half2'
          }
        ]
      }
    ]
  }, {
    questions: [
      {
        key: 'picture',
        type: contents.PICTURE,
        heading: 'Add a photo',
        text: 'Optional',
        error: 'Picture is wrong format',
        required: false,
      }
    ]
  }, {
    questions: [
      {
        key: 'comments',
        type: contents.COMMENTS,
        heading: 'Add a comment',
        text: 'Optional',
        required: false,
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