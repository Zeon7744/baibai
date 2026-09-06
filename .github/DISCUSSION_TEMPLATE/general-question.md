name: General Question
labels: ["question"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Have a question about the project? Ask here!
  - type: input
    id: title
    attributes:
      label: Title
      description: Brief summary of your question.
      placeholder: e.g. How to configure MCP for Cursor?
    validations:
      required: true
  - type: textarea
    id: question
    attributes:
      label: Question
      description: What would you like to know?
      placeholder: Describe your question in detail...
    validations:
      required: true
  - type: textarea
    id: context
    attributes:
      label: Context
      description: Any additional context or screenshots.
  - type: checkboxes
    id: search
    attributes:
      label: Search
      options:
        - label: I have searched existing issues.
          required: true
