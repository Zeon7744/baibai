name: New Issue
labels: ["triage"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Before opening an issue, please search existing ones to avoid duplicates.
  - type: dropdown
    id: type
    attributes:
      label: Issue Type
      options:
        - Bug Report
        - Feature Request
        - Documentation
        - Other
      default: 0
    validations:
      required: true
  - type: input
    id: title
    attributes:
      label: Title
      placeholder: Clear and concise title
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Description
      placeholder: Detailed description...
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: OS, Python version, dependencies.
      placeholder: |
        - OS: 
        - Python: 
        - Key packages:
    validations:
      required: false
  - type: textarea
    id: logs
    attributes:
      label: Logs / Screenshots
      description: Error output or relevant images.
      render: text
    validations:
      required: false
