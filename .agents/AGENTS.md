# Customization Rules - Swift Science Coding Agent

This file contains workspace-specific rules and instructions for coding assistants pair-programming on this repository.

## State Standard Activity Implementation
* **Rule**: When creating, extending, or implementing any new state standard activity or question set:
  * You **MUST** read and adhere to the baseline design template outlined in [activity_standard_design.md](file:///c:/Users/swift/edapp/planning/activity_standard_design.md).
  * Ensure each activity includes a 3-question quiz (drawn from a bank of 10), and a conditional lock/unlock mechanism on the workspace below it.
  * Register telemetry events `dok[X]_activity_check` and `dok[X]_activity_complete` correctly.
