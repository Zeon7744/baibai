name: Show and Tell
labels: ["show-and-tell"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Share what you built using this project! Get feedback and connect with others.
  - type: input
    id: title
    attributes:
      label: Project Title
      description: What did you build?
      placeholder: e.g. My ML-powered trading bot using crypto-mlp
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Tell us about your project and how you used this library.
      placeholder: What problem does it solve? What features did you add?
    validations:
      required: true
  - type: input
    id: link
    attributes:
      label: Links
      description: Links to your project, demo, or screenshots.
      placeholder: https://github.com/your/project
  - type: textarea
    id: feedback
    attributes:
      label: Feedback Requested
      description: What kind of feedback are you looking for?
      placeholder: Performance tips, feature suggestions, code review...
