'use strict';

const assert = require('assert');
const {
  resolveBuildLayoutAppId,
  resolveBuildLayoutPath,
  isBuildLayout,
  layoutForWrite,
} = require('./build-layout-docs-route');

const LAYOUT = {
  appId: 'build-playground',
  route: '#/build-playground',
  stage: { width: 932, height: 360 },
  revision: 4,
  elements: [
    {
      id: 'intro-text',
      role: 'text',
      placeholder: 'Intro',
      status: 'planned',
      rect: { xPct: 10, yPct: 12, wPct: 40, hPct: 15 },
    },
  ],
};

assert.strictEqual(resolveBuildLayoutAppId('/__layout/build/build-playground'), 'build-playground');
assert.strictEqual(resolveBuildLayoutAppId('/__layout/build/../secret'), null);
assert.strictEqual(resolveBuildLayoutAppId('/__layout/factoring-guided-portal'), null);
assert.ok(String(resolveBuildLayoutPath('build-playground')).endsWith('buildLayout.json'));
assert.strictEqual(resolveBuildLayoutPath('no-such-app'), null);
assert.ok(isBuildLayout(LAYOUT));
assert.ok(!isBuildLayout({ ...LAYOUT, elements: [{ ...LAYOUT.elements[0], role: 'button' }] }));

const written = layoutForWrite(LAYOUT, { ...LAYOUT, revision: 99 }, 'build-playground');
assert.strictEqual(written.ok, true);
assert.strictEqual(written.layout.revision, 5);
assert.strictEqual(written.layout.elements[0].id, 'intro-text');

const mismatch = layoutForWrite(LAYOUT, { ...LAYOUT, appId: 'other' }, 'build-playground');
assert.strictEqual(mismatch.ok, false);

console.log('build-layout-docs-route tests passed');
