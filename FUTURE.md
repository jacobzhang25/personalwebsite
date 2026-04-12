# FUTURE.md

Architectural notes for the planned tree / branching visualization of the blog. This file is a letter to future-me (or future-Claude) explaining *why* things are where they are, so that adding the visualization later is a drop-in change and not a rewrite.

## The vision

The `/blog` page should eventually be an interactive, creative visualization — a tree or branching structure where each **branch is a "sphere" of thinking** (work, spirituality, creativity, technology, personal), and individual posts are **leaves / nodes hanging off the relevant branch**. Clicking a node opens the post.

Likely candidates for implementation:

- **D3.js** — tree/cluster layouts, full control, steeper ceiling
- **React Flow** — node-based UI, easier to get interactive immediately, good for drag/pan/zoom
- **Svelte + D3** — if I want animation to feel effortless

Any of these will work. The current scaffold doesn't force a choice.

## The three architectural decisions that make this possible

### 1. `sphere` is typed and validated at build time

In `src/content/config.ts`:

```ts
export const SPHERES = [
  'work',
  'spirituality',
  'creativity',
  'technology',
  'personal',
] as const;
```

This array is the single source of truth. Adding a new branch to the tree is literally a one-line edit. The Zod schema enforces that every post uses a known value, so invalid data **fails the build** instead of silently breaking the visualization.

Future-me: when you add the viz, import `SPHERES` from the same file. Don't redefine the list.

### 2. `PostList.astro` is the single, isolated swap point

`/src/pages/blog/index.astro` does exactly two things:

1. Fetch all published posts via `getCollection('blog')`.
2. Pass them to `<PostList posts={posts} />`.

That's it. No other component touches the post data. When the tree viz is ready, the change is:

```diff
- import PostList from '../../components/PostList.astro';
+ import TreeVisualization from '../../components/TreeVisualization.jsx';
  ...
- <PostList posts={posts} />
+ <TreeVisualization client:load posts={posts} />
```

The data shape stays identical. Nothing else in the site needs to change.

**Important:** resist the urge to put logic in `blog/index.astro`. Keep it a thin shell. If you need to group posts by sphere, do that inside the visualization component — it's presentation, not data.

### 3. Astro islands hydrate the viz in isolation

Astro's whole value proposition here is that the rest of the site stays zero-JS static HTML, and *only* the tree visualization ships a JavaScript runtime to the browser. That's the `client:load` (or `client:visible`) directive in the diff above.

To actually install a framework when you're ready:

```bash
npx astro add react      # or: svelte, vue, solid, preact
```

This automatically updates `astro.config.mjs`, installs the integration, and adds the right tsconfig paths. Then create `src/components/TreeVisualization.jsx` and import it with a `.jsx` extension.

## The data shape you'll consume

`CollectionEntry<'blog'>` from `astro:content` gives you each post as:

```ts
{
  id: string;           // e.g. "hello-world.md"
  slug: string;         // e.g. "hello-world"
  data: {
    title: string;
    description: string;
    pubDate: Date;
    updatedDate?: Date;
    sphere: 'work' | 'spirituality' | 'creativity' | 'technology' | 'personal';
    tags: string[];
    draft: boolean;
  };
  // plus a render() method if you need the body
}
```

For the visualization you almost certainly only need `{ slug, data.title, data.sphere, data.pubDate, data.description }`. Consider transforming the collection into a flat array inside `blog/index.astro` *only if* you need to shed the extra fields before passing to the client — Astro will serialize the whole object as JSON when hydrating the island, and that costs bytes.

Suggested transform shape when you get there:

```ts
const nodes = posts.map((p) => ({
  slug: p.slug,
  title: p.data.title,
  description: p.data.description,
  pubDate: p.data.pubDate,
  sphere: p.data.sphere,
}));
```

## The tree data structure (sketch)

A simple transformation for a hierarchical layout (what D3's `d3.hierarchy` expects):

```ts
const root = {
  name: 'me',
  children: SPHERES.map((sphere) => ({
    name: sphere,
    children: nodes
      .filter((n) => n.sphere === sphere)
      .map((n) => ({ name: n.title, data: n })),
  })),
};
```

That's the whole data model. Feed `root` to `d3.hierarchy(root)` and pick your layout (`tree`, `cluster`, `pack`, etc.).

If you want something more organic — branches growing from a trunk, physics-based — React Flow with a custom layout or a D3 force simulation is the path. The data shape above still works for both.

## Styling guidance

The site's palette lives in CSS custom properties in `src/styles/global.css`:

```
--color-ink      # primary text
--color-ink-soft # secondary text
--color-paper    # background
--color-accent   # hover / highlight
--color-rule     # dividers
```

Use these in the visualization so it feels like part of the site rather than a bolted-on widget. Dark mode switches automatically via `prefers-color-scheme`.

## What NOT to do

- **Don't put the tree on the landing page.** The landing page is a personal essay site. The viz belongs at `/blog`.
- **Don't hardcode the list of spheres in the viz.** Import from `src/content/config.ts`.
- **Don't replace Markdown with a database.** The whole point is that posts are files you own. The viz reads files, it doesn't replace them.
- **Don't skip the fallback.** Keep `PostList.astro` around (even if unused in prod) so there's a working alternative if the viz breaks.

## Quick checklist when you're ready

- [ ] `npx astro add react` (or svelte/solid)
- [ ] Create `src/components/TreeVisualization.jsx`
- [ ] Import `SPHERES` from `src/content/config.ts`
- [ ] Consume `posts: CollectionEntry<'blog'>[]` (or a trimmed version) as a prop
- [ ] Swap one line in `src/pages/blog/index.astro`
- [ ] Verify static HTML still works with JS disabled (SSR fallback)
- [ ] Test on mobile — the viz should degrade gracefully or provide a list toggle
