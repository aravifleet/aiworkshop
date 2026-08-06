# Use cases generated from temporaryfile.md
URL: https://practicetestautomation.com/practice-test-login/

## Happy path: basic flow
Type: happy
Description: Validate the happy path on https://practicetestautomation.com/practice-test-login/ using the provided instructions.
Instructions:
- fill username with student
- fill password with Password123
- click login
- verify page loads
- capture DOM after login
- verify links are visible

## Negative path: invalid input or missing action
Type: negative
Description: Validate expected failures when inputs are missing or invalid.
Instructions:
- fill username with invalid_user
- fill password with invalid_pass
- click login
- verify error message appears

## Edge case: boundary or alternate navigation
Type: edge
Description: Verify edge cases and alternate navigation from the same starting point.
Instructions:
- verify navigation is stable
- capture DOM after each major step
- verify links are visible
