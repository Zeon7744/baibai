name: Pull Request
title: "PR: "
labels: []
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Thanks for submitting a PR! Please fill out the form below.
  - type: input
    id: title
    attributes:
      label: Title
      description: Add a descriptive title for your PR.
      placeholder: Add feature X
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear and concise description of what this PR changes.
      placeholder: Describe the changes...
    validations:
      required: true
  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I have read the CONTRIBUTING guide
        - label: I have added tests for my changes
        - label: I have updated documentation (if needed)
        - label: My changes generate no new warnings
  - type: textarea
    id: related
    attributes:
      label: Related Issues
      description: Link any related issues or discussions.
      placeholder: Fixes #123
