/**
 * Build-mode layout files on the Programs docs server (port 8765).
 * One allowlisted path per app. Do not add a second write mechanism.
 * Used by scripts/serve-programs-docs.js.
 */
'use strict';

const path = require('path');

const PROGRAMS_ROOT = path.join(__dirname, '..');

const BUILD_LAYOUT_FILES = {
  'build-playground': path.join(
    PROGRAMS_ROOT,
    'School Scrips',
    'student-portal',
    'src',
    'features',
    'build-playground',
    'buildLayout.json',
  ),
};

const BUILD_LAYOUT_PREFIX = '/__layout/build/';

function resolveBuildLayoutAppId(rel) {
  if (typeof rel !== 'string' || !rel.startsWith(BUILD_LAYOUT_PREFIX)) {
    return null;
  }
  const appId = rel.slice(BUILD_LAYOUT_PREFIX.length);
  if (!appId || appId.includes('/') || appId.includes('\\') || !/^[a-z0-9-]+$/.test(appId)) {
    return null;
  }
  return appId;
}

function resolveBuildLayoutPath(appId) {
  if (typeof appId !== 'string' || !Object.prototype.hasOwnProperty.call(BUILD_LAYOUT_FILES, appId)) {
    return null;
  }
  return BUILD_LAYOUT_FILES[appId];
}

function isFiniteNumber(value) {
  return typeof value === 'number' && Number.isFinite(value);
}

function isRectPct(value) {
  if (typeof value !== 'object' || value === null) {
    return false;
  }
  return (
    isFiniteNumber(value.xPct) &&
    isFiniteNumber(value.yPct) &&
    isFiniteNumber(value.wPct) &&
    isFiniteNumber(value.hPct)
  );
}

function isBuildElement(value) {
  if (typeof value !== 'object' || value === null) {
    return false;
  }
  if (typeof value.id !== 'string' || !value.id.trim()) {
    return false;
  }
  if (value.role !== 'text') {
    return false;
  }
  if (value.status !== 'planned' && value.status !== 'implemented') {
    return false;
  }
  if (value.placeholder !== undefined && typeof value.placeholder !== 'string') {
    return false;
  }
  return isRectPct(value.rect);
}

function isBuildLayout(value) {
  if (typeof value !== 'object' || value === null) {
    return false;
  }
  if (typeof value.appId !== 'string' || !value.appId.trim()) {
    return false;
  }
  if (typeof value.route !== 'string') {
    return false;
  }
  if (!isFiniteNumber(value.revision)) {
    return false;
  }
  const stage = value.stage;
  if (typeof stage !== 'object' || stage === null) {
    return false;
  }
  if (!isFiniteNumber(stage.width) || !isFiniteNumber(stage.height)) {
    return false;
  }
  if (!Array.isArray(value.elements) || !value.elements.every(isBuildElement)) {
    return false;
  }
  const ids = value.elements.map((element) => element.id.trim());
  return new Set(ids).size === ids.length;
}

function canonicalLayout(incoming, appId, revision) {
  return {
    appId,
    route: incoming.route,
    stage: { width: incoming.stage.width, height: incoming.stage.height },
    revision,
    elements: incoming.elements.map((element) => ({
      id: element.id.trim(),
      role: 'text',
      ...(typeof element.placeholder === 'string' ? { placeholder: element.placeholder } : {}),
      status: element.status,
      rect: {
        xPct: element.rect.xPct,
        yPct: element.rect.yPct,
        wPct: element.rect.wPct,
        hPct: element.rect.hPct,
      },
    })),
  };
}

function layoutForWrite(current, incoming, appId) {
  if (!isBuildLayout(incoming)) {
    return { ok: false, error: 'invalid layout shape' };
  }
  if (incoming.appId !== appId) {
    return { ok: false, error: 'appId does not match the route' };
  }
  if (current && typeof current === 'object' && current.appId && current.appId !== appId) {
    return { ok: false, error: 'file appId does not match the route' };
  }
  const currentRevision =
    current && typeof current === 'object' && isFiniteNumber(current.revision) ? current.revision : 0;
  return { ok: true, layout: canonicalLayout(incoming, appId, currentRevision + 1) };
}

module.exports = {
  BUILD_LAYOUT_PREFIX,
  resolveBuildLayoutAppId,
  resolveBuildLayoutPath,
  isBuildLayout,
  layoutForWrite,
};
