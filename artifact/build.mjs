// Builds the self-contained gate-calculator.html by inlining dec.mjs + gate.mjs + the statutory
// rates into the template. The inlined gate is the SAME parity-tested source (tests/test_js_gate_parity.py),
// so the Artifact cannot drift from the Python core. Do not hand-edit gate-calculator.html — run this.
import { readFileSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "..");

// Strip ES import/export so both modules live in one inline <script> scope.
const strip = (src) => src.split("\n")
  .filter((l) => !l.trim().startsWith("import "))
  .map((l) => l.replace(/^export\s+/, ""))
  .join("\n");

const dec = strip(readFileSync(join(here, "dec.mjs"), "utf8"));
const gate = strip(readFileSync(join(here, "gate.mjs"), "utf8"));
const rates = readFileSync(join(root, "config", "statutory_rates.json"), "utf8").trim();
const tpl = readFileSync(join(here, "gate-calculator.template.html"), "utf8");

const html = tpl
  .replace("/*INLINE_DEC*/", () => dec)
  .replace("/*INLINE_GATE*/", () => gate)
  .replace("/*INLINE_RATES*/", () => rates);

writeFileSync(join(here, "gate-calculator.html"), html);
console.log("built artifact/gate-calculator.html (" + html.length + " bytes)");
