// Self-test for dec.mjs — the BigInt fixed-scale decimal that must reproduce the Python core's
// money math for the JS-paise gate Artifact. Exits non-zero on any failure; prints OK on success.
import { fromString, add, sub, mul, div, quantize, toFixed, cmp } from "./dec.mjs";

let failures = 0;
function eq(got, want, label) {
  if (got !== want) { failures++; console.error(`FAIL ${label}: got ${got} want ${want}`); }
}

eq(toFixed(fromString("1.5"), 2), "1.50", "fromString/toFixed");
eq(toFixed(fromString("-1.5"), 2), "-1.50", "negative");
eq(toFixed(add(fromString("0.1"), fromString("0.2")), 2), "0.30", "add 0.1+0.2");
eq(toFixed(sub(fromString("1.00"), fromString("0.30")), 2), "0.70", "sub");
eq(toFixed(mul(fromString("100000"), fromString("0.0000307")), 2), "3.07", "mul turnover*exch");
eq(toFixed(mul(fromString("1000"), fromString("0.001")), 2), "1.00", "mul stt delivery");
eq(toFixed(div(fromString("4"), fromString("100000")), 8), "0.00004000", "div breakeven-ish");
eq(toFixed(quantize(fromString("2.005"), 2, "half_up"), 2), "2.01", "quantize half_up .005");
eq(toFixed(quantize(fromString("0.125"), 2, "half_even"), 2), "0.12", "quantize half_even .125->even");
eq(toFixed(quantize(fromString("0.135"), 2, "half_even"), 2), "0.14", "quantize half_even .135->even");
eq(cmp(fromString("1.0"), fromString("2.0")) < 0, true, "cmp lt");
eq(cmp(fromString("2.0"), fromString("2.0")) === 0, true, "cmp eq");

if (failures) { console.error(`${failures} failure(s)`); process.exit(1); }
console.log("OK");
