import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { formatPercent, formatDuration, formatBytes, formatNumber } from '../src/shared/utils/formatters.js';

describe('Formatters Utility Suite', () => {
  describe('formatPercent', () => {
    it('should format numbers to default 1 decimal place percentage', () => {
      assert.equal(formatPercent(92.4), '92.4%');
      assert.equal(formatPercent(50), '50.0%');
    });

    it('should respect custom decimal places', () => {
      assert.equal(formatPercent(92.456, 2), '92.46%');
      assert.equal(formatPercent(92, 0), '92%');
    });

    it('should handle null, undefined, or empty values safely', () => {
      assert.equal(formatPercent(null), '0%');
      assert.equal(formatPercent(undefined), '0%');
    });
  });

  describe('formatDuration', () => {
    it('should format minutes with min suffix', () => {
      assert.equal(formatDuration(15), '15 min');
      assert.equal(formatDuration(6.4), '6.4 min');
    });

    it('should handle zero correctly', () => {
      assert.equal(formatDuration(0), '0 min');
    });

    it('should handle null and undefined safely', () => {
      assert.equal(formatDuration(null), '0 min');
      assert.equal(formatDuration(undefined), '0 min');
    });
  });

  describe('formatBytes', () => {
    it('should format byte sizes correctly into human readable strings', () => {
      assert.equal(formatBytes(0), '0 Bytes');
      assert.equal(formatBytes(1024), '1 KB');
      assert.equal(formatBytes(1048576), '1 MB');
      assert.equal(formatBytes(1073741824), '1 GB');
    });

    it('should handle falsy values gracefully', () => {
      assert.equal(formatBytes(null), '0 Bytes');
      assert.equal(formatBytes(undefined), '0 Bytes');
    });
  });

  describe('formatNumber', () => {
    it('should format numbers with standard numeric grouping', () => {
      assert.equal(formatNumber(1000), new Intl.NumberFormat().format(1000));
      assert.equal(formatNumber(4800000), new Intl.NumberFormat().format(4800000));
    });

    it('should return 0 for null or undefined', () => {
      assert.equal(formatNumber(null), '0');
      assert.equal(formatNumber(undefined), '0');
    });
  });
});
