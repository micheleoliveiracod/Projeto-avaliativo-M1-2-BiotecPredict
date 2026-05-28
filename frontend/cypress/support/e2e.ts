// Cypress E2E support file
// This file is loaded before each spec file

// Disable uncaught exception handling for development
Cypress.on('uncaught:exception', (err, runnable) => {
  // Return false to prevent Cypress from failing the test
  return false;
});

// Custom commands
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('/login');
  cy.get('input[type="email"]').type(email);
  cy.get('input[type="password"]').type(password);
  cy.get('button[type="submit"]').click();
  cy.url().should('not.include', '/login');
});

Cypress.Commands.add('uploadCSV', (fileName: string, fileContent: string) => {
  cy.get('input[type="file"]').selectFile({
    contents: Cypress.Buffer.from(fileContent),
    fileName: fileName,
    mimeType: 'text/csv',
  });
});

// Global test timeout
Cypress.config('defaultCommandTimeout', 10000);
