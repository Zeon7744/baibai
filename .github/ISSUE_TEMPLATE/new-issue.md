name: New Issue
labels: ["new-issue"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        ## Welcome! Please choose an issue template:
  - type: dropdown
    id: template
    attributes:
      label: Issue Type
      options:
        - Bug Report (.github/ISSUE_TEMPLATE/bug-report.md)
        - Feature Request (.github/ISSUE_TEMPLATE/feature-request.md)
        - General Question (.github/ISSUE_TEMPLATE/general-question.md)
      default: 0
    validations:
      required: true
  - type: textarea
    id: details
    attributes:
      label: Details
      description: Provide additional details about your issue.
      placeholder: More context or information...
  - type: checkboxes
    id: read
    attributes:
      label: Pre-flight Checklist
      options:
        - label: I have searched existing issues
          required: true
        - label: I have read the README and documentation
          required: true
        - label: This is a single, focused issue
          required: true
