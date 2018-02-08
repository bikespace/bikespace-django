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
        index: 1,
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
      },
      {
        key: 'picture',
        type: contents.PICTURE,
        heading: 'Add a photo',
        text: 'Optional',
        required: false,
        index: 2
      },
    ]
  }
]

export default questions;