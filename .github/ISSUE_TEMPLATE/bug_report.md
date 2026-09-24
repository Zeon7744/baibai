name: Bug Report
labels: ["bug"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to report a bug!
  - type: input
    id: version
    attributes:
      label: Version
      description: What version are you using?
      placeholder: e.g. v1.0.0
    validations:
      required: true
  - type: input
    id: environment
    attributes:
      label: Environment
      description: OS, Python version, key dependencies.
      placeholder: e.g. Windows 11, Python 3.10.11
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: A clear and concise description of what the bug is.
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How to reproduce the issue.
      placeholder: |
        1. Run `python main.py --symbol BTC/USDT`
        2. See error
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What did you expect?
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Error Logs / Screenshots
      description: Paste error output or attach screenshots.
      render: text
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - High (blocking)
        - Medium
        - Low
      default: 1
    validations:
      required: true
