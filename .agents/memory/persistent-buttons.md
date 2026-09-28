---
name: Persistent Discord buttons
description: Compatibility and single-dispatch requirements for existing vending messages.
---

Keep existing vending custom IDs compatible when changing button handlers; users require already-posted panels to work without recreation. Never register both dynamic and ordinary handlers for the same ID.

**Why:** Discord.py dispatches dynamic and ordinary views separately, so overlapping registrations can cause duplicate purchase processing. A database-derived startup list can also omit an older panel. On 2026-09-28 the user confirmed the persistent-button repair worked on existing panels.

**How to apply:** Test restart dispatch with a machine absent from the startup name list, and verify one callback per click. Missing inventory must return an explicit error, never be reconstructed from a public message.

Refresh all known existing messages in place, not only the newest panel. **Why:** Users retain older messages; reposting on stock changes left public stock counts stale even while the purchase menu read current inventory. Resolve or explicitly relink authentic stored inventory rather than copying counts from a stale embed.

Do not require a legacy panel's display title to equal its saved machine key. **Why:** Display titles can differ while its bot-authored custom ID still identifies valid products. **How to apply:** Prefer a saved message identity, otherwise accept an unambiguous custom ID with existing products; reject conflicts with another live machine rather than silently selling different goods.