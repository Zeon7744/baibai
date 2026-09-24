name: Release Announcement
labels: ["release"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        ## Release: v{{version}}
  - type: input
    id: version
    attributes:
      label: Version
      description: What version is being released?
      placeholder: v1.3.0
    validations:
      required: true
  - type: textarea
    id: summary
    attributes:
      label: Summary
      description: Brief summary of this release (2-3 sentences).
      placeholder: This release adds X feature and fixes Y bug...
    validations:
      required: true
  - type: textarea
    id: highlights
    attributes:
      label: Highlights
      description: Key changes and improvements.
      placeholder: |
        - Added: new feature X
        - Fixed: bug Y
        - Improved: performance Z
    validations:
      required: true
  - type: textarea
    id: breaking
    attributes:
      label: Breaking Changes
      description: Any breaking changes? Leave blank if none.
  - type: textarea
    id: upgrade
    attributes:
      label: Upgrade Guide
      description: Steps to upgrade to this version.
  - type: input
    id: download
    attributes:
      label: Download
      description: Link to release assets or installation command.
      placeholder: pip install baibai==1.3.0
  - type: textarea
    id: thanks
    attributes:
      label: Thanks
      description: Shoutouts to contributors.
