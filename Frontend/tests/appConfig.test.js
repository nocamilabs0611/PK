import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { ROLES, ROLE_PERMISSIONS, ROUTES, MENU_ITEMS } from '../src/config/appConfig.js';

describe('App Configuration & RBAC Suite', () => {
  it('should define admin and operator roles', () => {
    assert.equal(ROLES.ADMIN, 'admin');
    assert.equal(ROLES.OPERATOR, 'user');
  });

  it('should grant full administrative privileges to ADMIN role', () => {
    const adminPerms = ROLE_PERMISSIONS[ROLES.ADMIN];
    assert.ok(adminPerms);
    assert.equal(adminPerms.canManageUsers, true);
    assert.equal(adminPerms.canEditWarehouseConfig, true);
    assert.equal(adminPerms.canRetrainModel, true);
    assert.equal(adminPerms.canExportAuditLogs, true);
    assert.equal(adminPerms.canAccessAdminConsole, true);
  });

  it('should restrict dangerous administrative operations from OPERATOR role', () => {
    const operatorPerms = ROLE_PERMISSIONS[ROLES.OPERATOR];
    assert.ok(operatorPerms);
    assert.equal(operatorPerms.canManageUsers, false);
    assert.equal(operatorPerms.canEditWarehouseConfig, false);
    assert.equal(operatorPerms.canRetrainModel, false);
    assert.equal(operatorPerms.canAccessAdminConsole, false);
  });

  it('should contain all required route identifiers', () => {
    const expectedRoutes = [
      'OVERVIEW',
      'LIVE_MONITORING',
      'DIGITAL_TWIN',
      'PREDICTIONS',
      'ALERTS',
      'SIMULATION',
      'ANALYTICS',
      'REPORTS',
      'USERS',
      'CONFIG',
      'SETTINGS'
    ];
    for (const key of expectedRoutes) {
      assert.ok(ROUTES[key], `Missing route: ${key}`);
    }
  });

  it('should define operations and administrative menu categories', () => {
    assert.ok(Array.isArray(MENU_ITEMS.operations));
    assert.ok(MENU_ITEMS.operations.length > 0);
    const opRouteIds = MENU_ITEMS.operations.map(item => item.id);
    assert.ok(opRouteIds.includes(ROUTES.OVERVIEW));
    assert.ok(opRouteIds.includes(ROUTES.DIGITAL_TWIN));
  });
});
