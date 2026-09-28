---
name: Confirmation-time inventory
description: Compatibility rule for changing finite inventory from order-time reservation to confirmation-time consumption.
---

Persisted orders must distinguish legacy orders whose inventory was already removed from newer orders whose inventory is consumed after successful delivery. Pending PayPay links must not reserve inventory; allocate current stock only when delivery starts.

**Why:** Treating old pending orders as new reservations can double-count stock. The user reported that unconfirmed PayPay links prevented buying the displayed quantity and requested that unconfirmed orders stop occupying inventory.

**How to apply:** Preserve legacy consumed inventory, exclude only active uncommitted deliveries when allocating stock, and consume inventory exactly once on successful delivery. Recheck stock at confirmation, including for old uncommitted pending orders; never deliver stale pending allocations.