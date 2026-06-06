describe('Dashboard Page E2E Tests', () => {
  before(() => {
    // Garante que existe ao menos um batch processado para o dashboard exibir dados reais
    cy.visit('/');
    cy.get('input[type="file"]').selectFile('cypress/fixtures/sample.csv', { force: true });
    cy.contains(/Arquivo enviado com sucesso/, { timeout: 20000 }).should('be.visible');
  });

  beforeEach(() => {
    cy.visit('/dashboard');
    cy.contains('Dashboard Analítico', { timeout: 20000 }).should('be.visible');
  });

  it('should load dashboard page', () => {
    cy.contains('Dashboard Analítico').should('be.visible');
    cy.contains('Monitoramento de Processos de Manufatura').should('be.visible');
  });

  it('should display compliance score card', () => {
    cy.contains('h2', 'Compliance Score').should('be.visible');
    cy.contains(/^(ACCEPTABLE|WARNING|CRITICAL)$/).should('be.visible');
  });

  it('should display risk prediction card', () => {
    cy.contains('h2', 'Predição de Risco').should('be.visible');
    cy.contains(/^(LOW_RISK|MEDIUM_RISK|HIGH_RISK)$/).should('be.visible');
  });

  it('should display sensor section', () => {
    cy.contains('Variáveis de Sensores').should('be.visible');
    cy.contains('Temperatura').should('be.visible');
    cy.contains('pH').should('be.visible');
  });

  it('should display batch table with headers', () => {
    cy.get('table.batch-table').should('be.visible');
    cy.get('table.batch-table thead').within(() => {
      cy.contains('th', 'ID do Batch').should('be.visible');
      cy.contains('th', 'Data de Upload').should('be.visible');
      cy.contains('th', 'Compliance Score').should('be.visible');
      cy.contains('th', 'Predição de Risco').should('be.visible');
      cy.contains('th', 'Status').should('be.visible');
    });
  });

  it('should display navigation menu', () => {
    cy.get('nav').within(() => {
      cy.contains('a', 'Upload').should('be.visible');
      cy.contains('a', 'Dashboard').should('be.visible');
    });
  });

  it('should navigate back to upload page', () => {
    cy.contains('a', 'Upload').click();
    cy.location('pathname').should('eq', '/');
    cy.contains('Upload de Arquivo CSV').should('be.visible');
  });
});
