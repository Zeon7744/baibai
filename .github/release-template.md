name: Release Template
title: "Release v{{version}}"
labels: ["release"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        ## Release Checklist
  - type: checkboxes
    id: checklist
    attributes:
      label: Pre-release
      options:
        - label: Version bumped in pyproject.toml / package.json
        - label: CHANGELOG.md updated
        - label: All tests passing
        - label: Documentation updated
        - label: GitHub Release tag created
  - type: textarea
    id: changelog
    attributes:
      label: Changelog Summary
      description: Brief summary of changes for this release.
    validations:
      required: true
  - type: textarea
    id: migration
    attributes:
      label: Migration Notes
      description: Any breaking changes or migration steps for users.
  - type: input
    id: related
    attributes:
      label: Related Issues
      description: Link related issues or PRs.
      placeholder: Fixes #123
