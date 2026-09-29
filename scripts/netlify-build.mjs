import { cp, mkdir, rm } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');

await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });
await cp(join(root, 'frontend'), dist, { recursive: true });
await mkdir(join(dist, 'data'), { recursive: true });
await cp(join(root, 'data', 'probe'), join(dist, 'data', 'probe'), { recursive: true });

console.log(`Netlify bundle ready: ${dist}`);
