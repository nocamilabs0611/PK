import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { simulationService } from '../src/services/simulationService.js';
import apiClient from '../src/services/apiClient.js';

describe('Simulation Service Suite', () => {
  beforeEach(() => {
    apiClient.setUseMock(true);
  });

  it('should run baseline simulation and return valid before/after deltas', async () => {
    const result = await simulationService.runSimulation({
      agvCount: 18,
      orderVolumeChange: 0,
      closedAisles: []
    });

    assert.ok(result);
    assert.equal(result.success, true);
    assert.equal(result.before.risk, 87);
    assert.equal(result.after.risk, 87);
    assert.ok(result.impact);
  });

  it('should calculate higher risk when order surge occurs and aisles close', async () => {
    const surgeResult = await simulationService.runSimulation({
      agvCount: 18,
      orderVolumeChange: 50,
      closedAisles: ['AISLE-B']
    });

    assert.ok(surgeResult.after.risk > 87);
    assert.ok(surgeResult.impact.includes('Surge'));
  });

  it('should calculate lower risk when extra AGVs are deployed', async () => {
    const optimizedResult = await simulationService.runSimulation({
      agvCount: 26,
      orderVolumeChange: -20,
      closedAisles: []
    });

    assert.ok(optimizedResult.after.risk < 87);
    assert.ok(optimizedResult.impact.includes('Net Congestion Reduction'));
  });

  it('should return saved scenario templates', async () => {
    const scenarios = await simulationService.getSavedScenarios();
    assert.ok(Array.isArray(scenarios));
    assert.ok(scenarios.length >= 2);
    assert.equal(scenarios[0].id, 'SCEN-01');
  });
});
