import { defineCollection, z } from 'astro:content';

/**
 * Spheres are the top-level categories that will become branches
 * in the future tree visualization. Add new values here as your
 * thinking evolves — the build will fail if a post uses an unknown
 * sphere, which is the guardrail we want.
 */
export const SPHERES = [
  'work',
  'spirituality',
  'creativity',
  'technology',
  'personal',
] as const;

export type Sphere = (typeof SPHERES)[number];

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    // `sphere` drives the future tree visualization.
    // See FUTURE.md for the architectural rationale.
    sphere: z.enum(SPHERES),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
