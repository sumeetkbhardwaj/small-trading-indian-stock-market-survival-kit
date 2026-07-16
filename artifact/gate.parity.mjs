// Computes the JS-paise break-even for each parity case and prints them as JSON, so a pytest can
// assert byte-for-byte equality with the Python CLI's `kit.py breakeven`. Same rates file, same
// fixed 8dp HALF_EVEN quantization.
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import { statutoryBreakevenPct } from "./gate.mjs";
import { fromString, quantize, toFixed } from "./dec.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "..");
const rates = JSON.parse(readFileSync(join(root, "config", "statutory_rates.json"), "utf8"));
const cases = JSON.parse(readFileSync(join(root, "tests", "fixtures", "gate_parity_cases.json"), "utf8"));

const out = cases.map((c) => {
  const be = statutoryBreakevenPct(fromString(c.price), c.qty, c.segment, rates,
                                   fromString(c.brokerage), fromString(c.dp));
  return toFixed(quantize(be, 8, "half_even"), 8);
});
console.log(JSON.stringify(out));
