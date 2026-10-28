const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');
const base = 'slides/ultralytics-map/resources/ultralytics-map/';
const ctx = {window: {}, deck: {cards: () => '', cover: () => ({}), end: () => ({})}};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(base + 'test-map-data.js', 'utf8'), ctx);
ctx.testAtlas = ctx.window.testAtlas;
vm.runInContext(fs.readFileSync(base + 'map-data.js', 'utf8') + fs.readFileSync(base + 'story.js', 'utf8') +
  ';globalThis.rendered=testAtlas.files.map(fileDetail);globalThis.pages=story.pages;', ctx);
assert.equal(ctx.rendered.length, ctx.testAtlas.files.length);
assert(ctx.rendered.every(x => !x.includes('undefined')));
for (const f of ctx.testAtlas.files.filter(f => f.review)) {
  assert(/[\u3400-\u9fff]/.test(f.review.rationale), f.path);
  assert(!/\?{3}/.test(JSON.stringify(f.review)), f.path);
  assert(f.review.starts.length, f.path);
}
for (const f of ctx.testAtlas.files.filter(f => f.coverage)) {
  assert.equal(f.coverage.hits + f.coverage.misses, f.coverage.lines);
  assert.equal(f.gaps.reduce((sum, g) => sum + g.lines.length, 0), f.coverage.misses);
}
console.log(`PASS: ${ctx.rendered.length} file cards, ${ctx.testAtlas.files.filter(f => f.review).length} reviews, ${ctx.testAtlas.files.flatMap(f => f.crosscheck).length} gap candidates, ${ctx.pages.length} pages`);
