// Runs the JS evaluate() over the golden CASES and prints {name: result}, for a pytest to assert
// byte-for-byte equality with golden_expected.json (the Python CLI's output). Same rates file.
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import { evaluate } from "./gate.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "..");
const rates = JSON.parse(readFileSync(join(root, "config", "statutory_rates.json"), "utf8"));
const cases = JSON.parse(readFileSync(join(root, "tests", "fixtures", "golden_cases.json"), "utf8"));

const out = {};
for (const [name, c] of Object.entries(cases)) out[name] = evaluate(c, rates);
console.log(JSON.stringify(out));
