import contents from './contents/contents';

const questions = [
  {
    questions: [
      {
        key: 'problem_type',
        type: contents.ISSUES,
        heading: 'What was the issue?',
        text: 'Choose whichever applies',
        required: true,
        error: 'Choose at least one option',
        values: [
          {
            key: 'absent',
            text: "No bike parking nearby"
          },
          {
            key: 'full',
            text: "Nearby bike parking is full"
          },
          {
            key: 'broken',
            text: "Bike parking is broken"
          },
          {
            key: 'unusable',
            text: "Bike parking is inaccessible or unusable"
          },
          {
            key: 'abandoned',
            text: "Report an abandoned bike"
          },
          {
            key: 'vandalized',
            text: "My bike was vandalized"
          },
          {
            key: 'stolen',
            text: "My bike was stolen"
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
        error: 'Picture is wrong format',
        required: false,
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
            key: '>1hour',
            text: "Less than 1 hour",
            class: 'half1'
          },
          {
            key: '1-2hours',
            text: "1 to 2 hours",
            class: 'half2'
          },
          {
            key: '4-8hours',
            text: "4 to 8 hours",
            class: 'half1'
          },
          {
            key: 'overnight+',
            text: "Overnight or longer",
            class: 'half2'
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