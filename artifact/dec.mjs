// dec.mjs — BigInt fixed-scale decimal for the JS-paise gate Artifact. Money is exact integers
// (float is banned, exactly as in the Python core's money.py). Internal scale = 20 decimal places;
// values are BigInt = value * 10^SCALE. mul/div round half-even; quantize takes the mode. Outputs
// are quantized to a fixed display precision so every surface (Python, this JS) matches byte-for-byte.
export const SCALE = 20n;
const TEN = 10n;
const SCALE_F = TEN ** SCALE;

const pow10 = (n) => TEN ** BigInt(n);

export function fromString(s) {
  s = String(s).trim();
  let neg = false;
  if (s[0] === "+") s = s.slice(1);
  if (s[0] === "-") { neg = true; s = s.slice(1); }
  let [intp, frac = ""] = s.split(".");
  intp = intp || "0";
  frac = (frac + "0".repeat(Number(SCALE))).slice(0, Number(SCALE));
  const v = BigInt(intp) * SCALE_F + BigInt(frac || "0");
  return neg ? -v : v;
}

export const add = (a, b) => a + b;
export const sub = (a, b) => a - b;
export const cmp = (a, b) => (a < b ? -1 : a > b ? 1 : 0);

// Divide num by den, rounding the quotient to an integer. mode: "half_up" | "half_even".
function roundedDiv(num, den, mode) {
  const neg = (num < 0n) !== (den < 0n);
  const n = num < 0n ? -num : num;
  const d = den < 0n ? -den : den;
  let q = n / d;
  const r = n % d;
  if (r !== 0n) {
    const twice = r * 2n;
    let up;
    if (twice > d) up = true;
    else if (twice < d) up = false;
    else up = mode === "half_up" ? true : (q % 2n === 1n); // half_even: round to even
    if (up) q += 1n;
  }
  return neg ? -q : q;
}

export const mul = (a, b) => roundedDiv(a * b, SCALE_F, "half_even");
export const div = (a, b) => roundedDiv(a * SCALE_F, b, "half_even");

// Round to `places` decimals with `mode`, returning a scaled value zeroed beyond `places`.
export function quantize(x, places, mode) {
  const f = pow10(SCALE - BigInt(places));
  return roundedDiv(x, f, mode) * f;
}

// String with exactly `places` decimals (quantize first for rounding; this truncates any residue).
export function toFixed(x, places) {
  const neg = x < 0n;
  const v = neg ? -x : x;
  const scaled = v / pow10(SCALE - BigInt(places));
  const s = scaled.toString().padStart(places + 1, "0");
  const cut = s.length - places;
  const intp = s.slice(0, cut) || "0";
  const frac = places > 0 ? "." + s.slice(cut) : "";
  return (neg && scaled !== 0n ? "-" : "") + intp + frac;
}
