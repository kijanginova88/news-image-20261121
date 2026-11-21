// news-image-20261121 — entry runner.
//
// What this does: it takes the finished newspaper image, entry.png,
// which lives in the same folder as this file, and places an exact
// byte-for-byte copy of it into the grading output folder.
//
// How to run it locally:
//   MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts
// If MAKEFUN_OUTPUT_DIR is not set, the copy lands in /output.
// The result is deterministic: the output file is always identical
// to entry.png, because nothing is re-encoded or re-rendered.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const folderOfThisFile = dirname(fileURLToPath(import.meta.url));
const pictureToShip = join(folderOfThisFile, "entry.png");

const targetFolder =
  process.env.MAKEFUN_OUTPUT_DIR && process.env.MAKEFUN_OUTPUT_DIR.length > 0
    ? process.env.MAKEFUN_OUTPUT_DIR
    : "/output";

mkdirSync(targetFolder, { recursive: true });

const destinationPath = join(targetFolder, "entry.png");
copyFileSync(pictureToShip, destinationPath);

console.log(`Wrote ${destinationPath}`);
