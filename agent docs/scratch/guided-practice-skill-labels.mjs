/**
 * Seven miss-badge categories for guided practice.
 * One badge per miss instance — tallied per student and class-wide.
 */

/** Short label on the badge itself. */
export const BADGE_LABELS = {
  'target-cell': 'Target cell',
  'transform-type': 'Transform type',
  'scaling-notation': 'Scaling notation',
  'replacement-notation': 'Replacement notation',
  'scaling-math': 'Scaling math',
  'replacement-math': 'Replacement math',
  solution: 'Solution',
};

/** Longer label in expanded detail panels. */
export const BADGE_DESCRIPTIONS = {
  'target-cell': 'Tapped the wrong matrix entry (for making a 1 or a 0)',
  'transform-type': 'Picked the wrong row transformation type',
  'scaling-notation': 'Row scaling notation wrong',
  'replacement-notation': 'Row replacement notation wrong',
  'scaling-math': 'Row scaling arithmetic wrong',
  'replacement-math': 'Row replacement arithmetic wrong',
  solution: 'Solution (x, y) wrong',
};

/** @deprecated alias — aggregate page uses BADGE_LABELS */
export const AGGREGATE_LABELS = BADGE_LABELS;

function opMeta(slot) {
  const match = slot.match(/^op([1-4])-(pick-cell|operation-type|row-notation|row-entry)$/);
  if (!match) return null;
  const opNum = Number(match[1]);
  const step = match[2];
  const isScale = opNum === 1 || opNum === 3;
  return { step, isScale };
}

export function skillForSlot(slot) {
  if (slot === 'solution') {
    return {
      category: 'solution',
      badgeLabel: BADGE_LABELS.solution,
      description: BADGE_DESCRIPTIONS.solution,
    };
  }

  const meta = opMeta(slot);
  if (!meta) {
    return {
      category: 'other',
      badgeLabel: slot,
      description: slot,
    };
  }

  const { step, isScale } = meta;

  if (step === 'pick-cell') {
    return {
      category: 'target-cell',
      badgeLabel: BADGE_LABELS['target-cell'],
      description: BADGE_DESCRIPTIONS['target-cell'],
    };
  }

  if (step === 'operation-type') {
    return {
      category: 'transform-type',
      badgeLabel: BADGE_LABELS['transform-type'],
      description: BADGE_DESCRIPTIONS['transform-type'],
    };
  }

  if (step === 'row-notation') {
    const category = isScale ? 'scaling-notation' : 'replacement-notation';
    return {
      category,
      badgeLabel: BADGE_LABELS[category],
      description: BADGE_DESCRIPTIONS[category],
    };
  }

  if (step === 'row-entry') {
    const category = isScale ? 'scaling-math' : 'replacement-math';
    return {
      category,
      badgeLabel: BADGE_LABELS[category],
      description: BADGE_DESCRIPTIONS[category],
    };
  }

  return {
    category: 'other',
    badgeLabel: slot,
    description: slot,
  };
}

export function aggregateCategoryOrder() {
  return Object.keys(BADGE_LABELS);
}

export const HELP_TOPIC_LABELS = {
  multiply: 'Fraction help — multiply',
  'add-subtract': 'Fraction help — add/subtract',
  'row-scaling': 'Row-scaling notation help',
  'row-replacement': 'Row-replacement notation help',
};

export const SURVEY_LABELS = [
  'When you got a step wrong, did the help make sense?',
  'Did you use the help buttons (fraction help, row notation help)?',
  'Would you use this again before a test?',
  'Anything else we should know?',
];

export const MCQ_LABELS = {
  no: 'No',
  maybe: 'Maybe',
  yes: 'Yes',
  didnt_use: "I didn't use it",
};
