name: Bug Report
labels: ["bug"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!
  - type: input
    id: version
    attributes:
      label: Version
      description: What version are you using?
      placeholder: e.g. v1.2.0
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: A clear and concise description of the bug.
      placeholder: Describe the issue...
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce the issue?
      placeholder: |
        1. Run '...'
        2. See error '...'
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What did you expect to happen?
  - type: dropdown
    id: severity
    attributes:
      label: Severity
      options:
        - Critical (blocking)
        - High (major impact)
        - Medium (minor issue)
        - Low (cosmetic)
      default: 2
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Relevant Log Output
      description: Please copy and paste any relevant log output.
      render: shell
  - type: checkboxes
    id: terms
    attributes:
      label: Code of Conduct
      options:
        - label: I agree to follow this project's Code of Conduct
          required: true
