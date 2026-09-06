name: Research Question
labels: ["research"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Ask a research question or discuss ideas for future development.
  - type: input
    id: topic
    attributes:
      label: Topic
      description: What area are you interested in exploring?
      placeholder: e.g. Adding ETH prediction support
    validations:
      required: true
  - type: textarea
    id: question
    attributes:
      label: Question
      description: Describe your research question or idea in detail.
    validations:
      required: true
  - type: textarea
    id: context
    attributes:
      label: Context
      description: Any background information, papers, or references.
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - High (blocking other work)
        - Medium (important)
        - Low (nice to have)
      default: 1
    validations:
      required: true
