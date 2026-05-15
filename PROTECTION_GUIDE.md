# מערכת זמן קבלית — Protection & Deployment Guide

---

## BEFORE YOU START — One required edit

Open `kabbalah-time-protected.html` in any text editor.
Find this line (around line 25):

```
'YOUR_GITHUB_USERNAME.github.io',
```

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username.
For example if your GitHub is `github.com/michaelg` change it to:
```
'michaelg.github.io',
```

Save the file. This is the domain lock — the code will silently refuse
to run on any other website.

---

## STEP 1 — Make your GitHub repo PRIVATE

1. Go to your GitHub repo
2. Click **Settings** (top right of repo)
3. Scroll to bottom → **Danger Zone**
4. Click **Change visibility** → **Make private**
5. Confirm

✓ Now nobody can see your source code on GitHub.

---

## STEP 2 — Enable GitHub Pages on a private repo

GitHub Pages works on private repos with a **free GitHub account**:

1. In your repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` → folder: `/ (root)`
4. Click **Save**

Your site will be live at:
`https://YOUR_GITHUB_USERNAME.github.io/REPO_NAME/`

✓ The page is publicly accessible but the SOURCE REPO is private.
  Nobody can browse your files on GitHub.

---

## STEP 3 — Upload the protected file

Replace your current `index.html` (or whatever your main file is called)
with `kabbalah-time-protected.html`, renamed to `index.html`.

```bash
# If using git on your computer:
cp kabbalah-time-protected.html index.html
git add index.html
git commit -m "Deploy protected version"
git push origin main
```

Or drag-and-drop the file directly in the GitHub web interface.

---

## STEP 4 — Verify the protection works

After deployment, visit your GitHub Pages URL and test:

| Test | Expected result |
|------|----------------|
| Right-click the page | Nothing happens (menu blocked) |
| Press F12 | Nothing happens |
| Press Ctrl+U | Nothing happens |
| Press Ctrl+S | Nothing happens |
| Open devtools manually via browser menu | Gold copyright warning appears in console |
| View page source | You see base64 chunks, not readable JS |
| Copy HTML and open locally | Domain lock triggers, page shows error |
| Someone copies to their server | Domain lock triggers, shows copyright error |

---

## WHAT SOMEONE SEES if they try to steal it

### In Page Source (Ctrl+U blocked, but if they use browser menu):
```
<!-- ©2025 Michael Gurshumov — All Rights Reserved... -->
const _chunks = ["bmRhaSBuaWFk","...","659 more unreadable chunks..."];
const _encoded = _chunks.join('');
const _fn = new Function(atob(_encoded));
_fn();
```
→ They see scrambled base64. No readable logic.

### If they copy the file and host it elsewhere:
→ Domain lock fires, page shows:
  "This software is licensed and may only run on its authorized domain.
   Unauthorized use violates copyright law.
   © 2025 Michael Gurshumov — All Rights Reserved."

### If they open DevTools:
→ Console shows in gold text:
  "© 2025 Michael Gurshumov — Proprietary Software. Inspection prohibited."

---

## LEGAL PROTECTION — DMCA Takedown Template

If someone steals your code and publishes it, send this to their hosting
provider (GitHub, Netlify, Vercel, etc.):

---

**Subject: DMCA Takedown Notice — Copyright Infringement**

To: [hosting provider abuse team, e.g. copyright@github.com]

I am the copyright owner of the software known as
"מערכת זמן קבלית (Kabbalistic Time System)".

The following URL contains my copyrighted work without authorization:
[INFRINGING URL]

My original work is located at:
[YOUR GITHUB PAGES URL]

I have a good faith belief that the use of my copyrighted work
described above is not authorized by me, my agent, or the law.

Under penalty of perjury, I state that the information in this
notification is accurate and that I am the copyright owner.

I request that you immediately remove or disable access to the
infringing material.

Name: Michael Gurshumov
Date: [TODAY'S DATE]
Contact: [YOUR EMAIL]

---

Send to:
- GitHub:   copyright@github.com
- Netlify:  abuse@netlify.com
- Vercel:   dmca@vercel.com
- Cloudflare: abuse@cloudflare.com

GitHub typically responds within 24 hours and removes infringing content.

---

## LIMITATIONS — What this does NOT protect against

Be honest with yourself about what's possible:

| Threat | Protected? |
|--------|-----------|
| Casual copy-paste theft | ✓ Yes — domain lock stops it |
| Someone saving your page | ✓ Yes — won't run elsewhere |
| Google indexing your code | ✓ Yes — private repo |
| A determined developer spending hours | ✗ No — base64 is reversible |
| Screen recording your app | ✗ No |
| Rebuilding from scratch after watching | ✗ No |

The base64 encoding is NOT encryption — a determined expert can decode it.
But it stops 99% of casual theft and gives you strong legal standing.

For maximum protection, the subscription-based backend (Firebase + payment
wall) we discussed is the real answer — even if someone extracts your JS,
it won't work without a valid subscription token from your server.

---

## MAINTENANCE

Every time you update `kabbalah-time.html`:
1. Re-run the protection script to regenerate `kabbalah-time-protected.html`
2. Push the new protected file to GitHub as `index.html`

Your working source (`kabbalah-time.html`) should NEVER be pushed
to any public repository. Keep it only on your local machine.
