# Customization Rules - Swift Science Coding Agent

This file contains workspace-specific rules and instructions for coding assistants pair-programming on this repository.

## State Standard Activity Implementation
* **Rule**: When creating, extending, or implementing any new state standard activity or question set:
  * You **MUST** read and adhere to the baseline design template outlined in [activity_standard_design.md](file:///c:/Users/swift/edapp/planning/activity_standard_design.md).
  * Ensure each activity includes a 3-question quiz (drawn from a bank of 10), and a conditional lock/unlock mechanism on the workspace below it.
  * Register telemetry events `dok[X]_activity_check` and `dok[X]_activity_complete` correctly.

## Cloud Cost & Egress Optimization Guidelines
* **Egress Minimization**: Offload all large WebAssembly compiles (like Pyodide) and heavy asset rendering natively to the browser (client-side execution). Egress costs for these must be $0.
* **Public CDN Offloading**: Load large library script packages (e.g. Pyodide, Chart.js, Tailwind, etc.) via public CDNs (Fastly/Cloudflare/unpkg) to completely bypass hosting server network output bills.
* **Telemetry Batching**: Batch telemetry requests (`dok[X]_activity_check` attempts) locally and save them to LocalStorage/State first. Sync them in a single aggregated transaction when completing a module (`dok[X]_activity_complete`), rather than making an API call for every button click.
* **Roster API Caching**: Cache third-party Google Classroom roster queries in session memory or client storage to avoid repeating API gateway hits on every page load.

