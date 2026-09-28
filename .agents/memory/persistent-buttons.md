---
name: Persistent Discord buttons
description: Compatibility and single-dispatch requirements for existing vending messages.
---

Keep existing vending custom IDs compatible when changing button handlers; users require already-posted panels to work without recreation. Never register both dynamic and ordinary handlers for the same ID.

**Why:** Discord.py dispatches dynamic and ordinary views separately, so overlapping registrations can cause duplicate purchase processing. A database-derived startup list can also omit an older panel.

**How to apply:** Test restart dispatch with a machine absent from the startup name list, and verify one callback per click. Missing inventory must return an explicit error, never be reconstructed from a public message.