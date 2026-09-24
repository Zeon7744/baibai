name: Feature Request
labels: ["enhancement"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Have an idea? Share it here!
  - type: input
    id: title
    attributes:
      label: Title
      description: Short descriptive title.
      placeholder: e.g. Add ETH prediction support
    validations:
      required: true
  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What problem does this solve?
  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How should this be implemented?
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives
      description: Any alternatives you considered.
  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Screenshots, references, etc.
