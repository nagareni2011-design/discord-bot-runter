---
name: GitHub and Railway access
description: Distinguish Railway's repository access from Replit's Git push credentials.
---

Railway's GitHub App authorization to watch and deploy a repository does not grant the Replit workspace or its Git CLI write access to that repository.

**Why:** A repo can appear in Railway's source picker while pushes from Replit still fail with a permission error. A successful Railway deployment can also be for a different repository than the source edited in this workspace.

**How to apply:** Before claiming a code change is deployed, verify the workspace can push to the exact owner/repository, then verify Railway is connected to that same repository and branch. Never force-push around an access error; keep the local commit and request the correct repository permission.
