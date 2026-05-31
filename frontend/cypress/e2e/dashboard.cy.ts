describe('Dashboard Page E2E Tests', () => {
  beforeEach(() => {
    cy.visit('/dashboard');
  });

  it('should load dashboard page', () => {
    cy.contains('Dashboard Analítico').should('be.visible');
  });

  it('should display compliance score card', () => {
    cy.get('[data-testid="compliance-score-card"]').should('be.visible');
    cy.get('[data-testid="compliance-score"]').should('contain', /\d+/);
  });

  it('should display risk prediction card', () => {
    cy.get('[data-testid="risk-prediction-card"]').should('be.visible');
    cy.get('[data-testid="risk-level"]').should('contain', /LOW|MEDIUM|HIGH/);
  });

  it('should display sensor charts', () => {
    cy.get('[data-testid="sensor-charts"]').should('be.visible');
    cy.get('canvas').should('have.length.greaterThan', 0);
  });

  it('should display batch table', () => {
    cy.get('[data-testid="batch-table"]').should('be.visible');
    cy.get('table').should('be.visible');
  });

  it('should display table headers', () => {
    cy.contains('ID').should('be.visible');
    cy.contains('Data Upload').should('be.visible');
    cy.contains('Status').should('be.visible');
    cy.contains('Compliance Score').should('be.visible');
    cy.contains('Risk Prediction').should('be.visible');
  });

  it('should navigate back to upload page', () => {
    cy.get('a').contains('Upload').click();
    cy.url().should('include', '/');
    cy.contains('Upload de Arquivo CSV').should('be.visible');
  });

  it('should display navigation breadcrumbs', () => {
    cy.get('[data-testid="breadcrumb"]').should('be.visible');
    cy.contains('Home').should('be.visible');
    cy.contains('Dashboard').should('be.visible');
  });
});
