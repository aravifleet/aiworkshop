# Adaptive Checkout Suite

This suite reads the active user story from `user-stories/`, discovers the live app flow, and writes:

- `artifacts/<story>-app-profile.json`
- `artifacts/<story>-gap-report.md`

## Run

From the repo root:

```powershell
npm run qa:adaptive
```

List discovered tests only:

```powershell
npm run qa:adaptive:list
```

## Use a Different User Story

If you have more than one markdown file in `user-stories/`, choose one with `USER_STORY_FILE`:

```powershell
$env:USER_STORY_FILE='user-stories\\my-other-story.md'; npm run qa:adaptive
```

## What It Adapts To

- Login page on the home page or a dedicated login route
- Product discovery from inventory grids or product-detail pages
- Cart access through a live cart control or a direct cart route
- Checkout entry and checkout-info field discovery

## What It Produces

- A discovered selector map for the live app
- A capability summary for login, add-to-cart, cart, checkout, and checkout form
- A gap report when the live app does not match the story expectations
