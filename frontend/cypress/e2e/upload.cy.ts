describe('Upload Page E2E Tests', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should load upload page', () => {
    cy.contains('Upload de Arquivo CSV').should('be.visible');
    cy.contains('Faça upload de um arquivo CSV').should('be.visible');
  });

  it('should display upload card', () => {
    cy.get('.upload-card').should('be.visible');
    cy.get('.upload-area').should('be.visible');
  });

  it('should upload a CSV via drag and drop, show success feedback and redirect to dashboard', () => {
    cy.get('.upload-area').selectFile('cypress/fixtures/sample.csv', { action: 'drag-drop' });

    cy.contains(/Arquivo enviado com sucesso/, { timeout: 20000 }).should('be.visible');
    cy.location('pathname', { timeout: 10000 }).should('eq', '/dashboard');
  });

  it('should show error for invalid file type', () => {
    cy.get('input[type="file"]').selectFile('cypress/fixtures/invalid.txt', { force: true });
    cy.contains('CSV válido').should('be.visible');
  });
});
