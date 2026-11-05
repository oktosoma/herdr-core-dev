const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');

// Execute the guide's actual inline script with a small DOM adapter. Layout is
// verified separately in Chromium; these tests exercise behavior/failure paths.
const html = fs.readFileSync(path.join(__dirname, '../../docs/guide/index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
function element(text = '', attrs = {}) {
  const classes = new Set();
  return {
    textContent: text, innerText: text, value: '', style: {}, handlers: {}, attrs,
    classList: {toggle(name, active) { if (active) classes.add(name); else classes.delete(name); }, contains: name => classes.has(name)},
    getAttribute: name => attrs[name] || null,
    setAttribute(name, value) { attrs[name] = value; },
    removeAttribute(name) { delete attrs[name]; },
    addEventListener(name, handler) { this.handlers[name] = handler; },
    focus() {}, select() {}, remove() {},
  };
}
function setup({clipboard, legacy = () => false} = {}) {
  const sections = [element('Purpose and roles'), element('Testing and integration')];
  sections.forEach((section, i) => { section.id = `s${i}`; });
  const links = sections.map(section => element('', {href: `#${section.id}`}));
  const ids = Object.fromEntries(['searchInput', 'noResult', 'searchStatus', 'copyStatus'].map(id => [id, element()]));
  const button = element('Copy');
  button.closest = () => ({querySelector: () => element('example command\n')});
  const window = {handlers: {}, addEventListener(name, handler) { this.handlers[name] = handler; }};
  const context = {
    window, navigator: {clipboard},
    document: {
      querySelectorAll: query => ({'#tocNav a': links, 'section.doc': sections, '.copybtn': [button]})[query],
      getElementById: id => ids[id],
      createElement: () => element(), body: {appendChild() {}}, execCommand: legacy,
    },
    setTimeout() { return 1; }, clearTimeout() {},
  };
  vm.runInNewContext(script, context);
  return {sections, links, ids, button, window};
}

test('search reports counts, hides nonmatches, and clear restores all sections', () => {
  const {sections, ids} = setup();
  ids.searchInput.value = 'integration';
  ids.searchInput.handlers.input();
  assert.equal(sections[0].classList.contains('hidden-by-search'), true);
  assert.equal(sections[1].classList.contains('hidden-by-search'), false);
  assert.equal(ids.searchStatus.textContent, '1 of 2 sections shown.');
  ids.searchInput.value = 'no-match';
  ids.searchInput.handlers.input();
  assert.equal(ids.noResult.style.display, 'block');
  ids.searchInput.value = '';
  ids.searchInput.handlers.input();
  assert.equal(sections.some(s => s.classList.contains('hidden-by-search')), false);
});

test('contents navigation reveals targets hidden by search', () => {
  const {sections, links, ids} = setup();
  ids.searchInput.value = 'no-match';
  ids.searchInput.handlers.input();
  links[0].handlers.click();
  assert.equal(ids.searchInput.value, '');
  assert.equal(sections[0].classList.contains('hidden-by-search'), false);
});

test('fragment navigation clears an active filter', () => {
  const {ids, window} = setup();
  ids.searchInput.value = 'no-match';
  ids.searchInput.handlers.input();
  window.handlers.hashchange();
  assert.equal(ids.searchInput.value, '');
});

test('confirmed clipboard write reports success and copies actual code', async () => {
  let copied;
  const {button, ids} = setup({clipboard: {writeText: async text => { copied = text; }}});
  await button.handlers.click();
  assert.equal(copied, 'example command');
  assert.equal(button.textContent, 'Copied ✓');
  assert.equal(ids.copyStatus.textContent, 'Code copied to clipboard.');
});

test('clipboard rejection reports failure instead of false success', async () => {
  const {button, ids} = setup({clipboard: {writeText: async () => { throw Error('denied'); }}});
  await button.handlers.click();
  assert.equal(button.textContent, 'Copy failed');
  assert.match(ids.copyStatus.textContent, /manually/);
});

test('legacy copy requires a true result and catches exceptions', async () => {
  for (const legacy of [() => false, () => { throw Error('denied'); }]) {
    const {button} = setup({legacy});
    await button.handlers.click();
    assert.equal(button.textContent, 'Copy failed');
  }
  const {button} = setup({legacy: () => true});
  await button.handlers.click();
  assert.equal(button.textContent, 'Copied ✓');
});

test('a stale clipboard request cannot overwrite a newer outcome', async () => {
  const pending = [];
  const {button} = setup({clipboard: {writeText: () => new Promise((resolve, reject) => pending.push({resolve, reject}))}});
  const old = button.handlers.click();
  const recent = button.handlers.click();
  pending[1].resolve();
  await recent;
  pending[0].reject(Error('old failure'));
  await old;
  assert.equal(button.textContent, 'Copied ✓');
});
