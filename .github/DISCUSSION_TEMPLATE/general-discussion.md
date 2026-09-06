name: General Discussion
labels: ["discussion"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        General discussion about the project, features, or community.
  - type: input
    id: title
    attributes:
      label: Title
      description: Brief summary of your discussion topic.
      placeholder: e.g. Thoughts on adding multi-timeframe analysis?
    validations:
      required: true
  - type: textarea
    id: content
    attributes:
      label: Content
      description: Start the discussion here.
      placeholder: Share your thoughts, questions, or ideas...
    validations:
      required: true
  - type: dropdown
    id: category
    attributes:
      label: Category
      options:
        - General Discussion
        - Feature Ideas
        - Community
        - Questions
      default: 0
    validations:
      required: true
