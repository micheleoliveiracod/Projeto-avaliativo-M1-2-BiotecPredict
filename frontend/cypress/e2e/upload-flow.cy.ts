describe('Upload Flow E2E Tests', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should navigate to upload page', () => {
    cy.contains('Upload').click();
    cy.url().should('include', '/upload');
    cy.contains('Upload CSV').should('be.visible');
  });

  it('should upload a CSV file successfully', () => {
    cy.visit('/upload');
    
    // Create a test CSV file
    const fileName = 'test-batch.csv';
    const fileContent = `temperature,ph,dissolved_oxygen,pressure,agitator_speed
37.5,7.2,85.3,2.1,250
38.0,7.1,84.5,2.2,255
36.8,7.3,86.1,2.0,248`;
    
    cy.get('input[type="file"]').selectFile({
      contents: Cypress.Buffer.from(fileContent),
      fileName: fileName,
      mimeType: 'text/csv',
    });
    
    cy.contains('Upload').click();
    cy.contains('Batch received', { timeout: 5000 }).should('be.visible');
  });

  it('should display batch in history after upload', () => {
    cy.visit('/');
    cy.contains('Batches').click();
    cy.url().should('include', '/batches');
    cy.get('table').should('be.visible');
  });

  it('should show batch details', () => {
    cy.visit('/');
    cy.contains('Batches').click();
    cy.get('table tbody tr').first().click();
    cy.url().should('include', '/batch/');
    cy.contains('Compliance Score').should('be.visible');
    cy.contains('Risk Prediction').should('be.visible');
  });

  it('should display compliance score on dashboard', () => {
    cy.visit('/');
    cy.contains('Dashboard').click();
    cy.url().should('include', '/dashboard');
    cy.contains('Compliance Score').should('be.visible');
    cy.get('[data-testid="compliance-score"]').should('exist');
  });

  it('should display risk prediction on dashboard', () => {
    cy.visit('/');
    cy.contains('Dashboard').click();
    cy.contains('Risk Prediction').should('be.visible');
    cy.get('[data-testid="risk-prediction"]').should('exist');
  });

  it('should filter batches by date', () => {
    cy.visit('/');
    cy.contains('Batches').click();
    cy.get('input[type="date"]').first().type('2026-05-24');
    cy.get('button').contains('Filter').click();
    cy.get('table tbody tr').should('have.length.greaterThan', 0);
  });

  it('should display charts on analytics page', () => {
    cy.visit('/');
    cy.contains('Analytics').click();
    cy.url().should('include', '/analytics');
    cy.get('canvas').should('exist');
  });
});
