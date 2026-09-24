name: Feature Request
labels: ["enhancement"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Suggest an idea for this project!
  - type: input
    id: title
    attributes:
      label: Title
      description: A short summary of your feature request.
      placeholder: e.g. Add ETH prediction support
    validations:
      required: true
  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: Is your feature request related to a problem?
  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: Describe the solution you'd like.
      placeholder: Would be great if...
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives
      description: Any alternative solutions you've considered.
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
  - type: checkboxes
    id: search
    attributes:
      label: Search
      options:
        - label: I have searched existing issues.
          required: true
