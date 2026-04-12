# personalwebsite

A minimal, typography-focused personal site and blog built with [Astro](https://astro.build).

- Markdown posts in `src/content/blog/`
- Typed frontmatter (schema in `src/content/config.ts`)
- Static output — deploys anywhere
- Designed so the blog index can later be replaced by an interactive tree visualization (see [`FUTURE.md`](./FUTURE.md))

---

## Requirements

- Node.js 20+ (tested on 22)
- npm (or pnpm / yarn — substitute as you like)

## Running locally

```bash
npm install
npm run dev      # starts dev server at http://localhost:4321
npm run build    # produces static output in ./dist
npm run preview  # serves the built site locally
```

## Project structure

```
.
├── astro.config.mjs
├── netlify.toml                # deploy config (delete if using Vercel)
├── public/
│   └── favicon.svg
├── src/
│   ├── content/
│   │   ├── config.ts           # typed frontmatter schema — edit SPHERES here
│   │   └── blog/
│   │       └── hello-world.md  # example post
│   ├── layouts/
│   │   ├── BaseLayout.astro    # shared HTML shell
│   │   └── PostLayout.astro    # wraps individual posts
│   ├── components/
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   ├── EmailSignup.astro   # PLACEHOLDER — see "Email signup" below
│   │   └── PostList.astro      # isolated swap point for the future tree viz
│   ├── pages/
│   │   ├── index.astro         # landing page
│   │   ├── blog/
│   │   │   ├── index.astro     # /blog listing
│   │   │   └── [...slug].astro # dynamic post pages
│   │   └── 404.astro
│   └── styles/
│       └── global.css
├── README.md
└── FUTURE.md
```

## Adding a new post

1. Create a new file in `src/content/blog/` — the filename becomes the URL slug.
   For example, `src/content/blog/on-rest.md` is served at `/blog/on-rest`.
2. Start it with frontmatter that matches the schema in `src/content/config.ts`:

   ```markdown
   ---
   title: "On rest"
   description: "A short note on why I stopped optimizing weekends."
   pubDate: 2026-04-20
   sphere: personal        # one of: work | spirituality | creativity | technology | personal
   tags:
     - rest
     - time
   draft: false            # drafts are shown in dev, hidden in production
   ---

   Your content here.
   ```

3. Write your post in Markdown below the frontmatter. `npm run dev` hot-reloads.
4. The build will **fail** if `sphere` is missing or uses an unknown value — that's the guardrail. Add new spheres to the `SPHERES` array in `src/content/config.ts`.

## Email signup

The signup form in `src/components/EmailSignup.astro` is a **placeholder**. It renders, but it doesn't actually collect anything yet. Open that file for step-by-step instructions to wire it up to:

- **ConvertKit** — paste form action URL
- **Buttondown** — paste username
- **Serverless endpoint** — if you want more control

A visible warning shows on the rendered form until you connect it. Remove the `<p class="placeholder-notice">...</p>` block once you're done.

## Deploying

The site is a plain static build. `npm run build` outputs `./dist`. Any static host will serve it. Two recommended options:

### Option A — Netlify (recommended)

1. Push this repo to GitHub.
2. Go to [app.netlify.com](https://app.netlify.com), click **Add new site → Import an existing project**, and select the repo.
3. Netlify auto-detects Astro. The `netlify.toml` in this repo already sets:
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Node version: 20
4. Click deploy. You'll get a `*.netlify.app` URL immediately.

### Option B — Vercel

1. Push this repo to GitHub.
2. Go to [vercel.com/new](https://vercel.com/new) and import the repo.
3. Vercel auto-detects Astro. No config needed. You can delete `netlify.toml` if you like.
4. Click deploy. You'll get a `*.vercel.app` URL immediately.

### Pointing your GoDaddy domain at the deployed site

Once you have a working deploy URL, add your custom domain:

**On Netlify:**
1. In your site dashboard → **Domain settings → Add custom domain** → enter your domain.
2. Netlify will show you DNS records to add. You have two choices:
   - **Easier:** Use Netlify DNS (they give you nameservers; you replace GoDaddy's nameservers with theirs in GoDaddy → **My Products → DNS → Nameservers → Change → Enter my own**).
   - **Keep GoDaddy DNS:** Add an `A` record at `@` pointing to `75.2.60.5` and a `CNAME` at `www` pointing to `<your-site>.netlify.app`. (Netlify shows the exact current values — use those, not these, in case they change.)
3. Netlify will auto-provision a Let's Encrypt certificate once DNS resolves.

**On Vercel:**
1. In your project → **Settings → Domains** → add your domain.
2. Vercel will show you one of two options:
   - An `A` record at `@` pointing to `76.76.21.21`
   - A `CNAME` at `www` pointing to `cname.vercel-dns.com`
3. Add those records in GoDaddy → **My Products → DNS → Manage DNS**.
4. SSL is automatic.

DNS propagation can take anywhere from a few minutes to 48 hours. You can check with `dig yourdomain.com` or [dnschecker.org](https://dnschecker.org).

## Things you'll want to replace

Grep for `TODO` and `Your Name` throughout the code. Hot spots:

- `astro.config.mjs` — change `site:` to your real domain
- `src/components/Header.astro` — replace `Your Name`
- `src/components/Footer.astro` — replace `Your Name`
- `src/pages/index.astro` — replace the Lorem Ipsum bio and the lede
- `public/favicon.svg` — replace the `Y` with your initial (or drop in your own SVG)
- `src/components/EmailSignup.astro` — connect to your provider

## What's next

See [`FUTURE.md`](./FUTURE.md) for the architectural notes on the planned tree visualization and how to plug it in without rewriting the site.
