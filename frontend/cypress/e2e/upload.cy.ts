describe('Upload Page E2E Tests', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should load upload page', () => {
    cy.contains('Upload de Arquivo CSV').should('be.visible');
    cy.contains('Faça upload de um arquivo CSV').should('be.visible');
  });

  it('should display upload card', () => {
    cy.get('[data-testid="upload-card"]').should('be.visible');
  });

  it('should handle drag and drop', () => {
    const fileName = 'sample.csv';
    cy.get('[data-testid="upload-area"]').selectFile('cypress/fixtures/sample.csv', {
      action: 'drag-drop',
    });
    cy.contains('Arquivo selecionado').should('be.visible');
  });

  it('should show success feedback after upload', () => {
    cy.get('[data-testid="upload-area"]').selectFile('cypress/fixtures/sample.csv', {
      action: 'drag-drop',
    });
    cy.get('[data-testid="upload-button"]').click();
    cy.contains('Upload realizado com sucesso').should('be.visible');
  });

  it('should redirect to dashboard after successful upload', () => {
    cy.get('[data-testid="upload-area"]').selectFile('cypress/fixtures/sample.csv', {
      action: 'drag-drop',
    });
    cy.get('[data-testid="upload-button"]').click();
    cy.url().should('include', '/dashboard');
  });

  it('should show error for invalid file', () => {
    cy.get('[data-testid="upload-area"]').selectFile('cypress/fixtures/invalid.txt', {
      action: 'drag-drop',
    });
    cy.contains('Arquivo inválido').should('be.visible');
  });
});
