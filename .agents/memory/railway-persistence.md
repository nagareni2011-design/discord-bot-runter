---
name: Railway JSON persistence verification
description: Distinguish missing runtime data from broken Discord panel routing before deploying fixes.
---

Verify the live storage mount and runtime save path before redeploying to diagnose missing custom products. A README recommending a volume is not evidence that the live service has one.

**Why:** Live inspection on 2026-09-28 found no volume and repeated full starter-catalog seeding after deployments. Existing Discord messages outlived their product records, so successive button fixes could not restore their contents.

**How to apply:** Check actual mounted volumes, runtime save-path logs, and current/backup product presence. Repeated complete template seeding indicates possible data resets, not successful recovery. Preserve accessible live data before storage changes or redeployment. Do not call seeded warning lines restored inventory or reconstruct delivery contents from public panels.