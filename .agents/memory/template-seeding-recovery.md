---
name: Template seeding recovery
description: Reliability rule for starter vending-machine catalog initialization on upgrades.
---

Starter catalog initialization should be idempotent and callable again from an admin entry point, not only during process startup. Routine startup should add missing machines without resetting sold inventory.

**Why:** A persistent JSON file can outlive a deployment, and a startup migration can be skipped or interrupted while the bot still becomes available. A later catalog correction must not refill stock after sales or alter an in-flight order.

**How to apply:** Seed absent machines and retry from admin entry points. If an explicitly requested catalog correction must overwrite known template rows, gate it behind a persisted catalog version, limit it to those templates, preserve IDs/history and panel mappings, and defer while affected orders are pending or delivering.