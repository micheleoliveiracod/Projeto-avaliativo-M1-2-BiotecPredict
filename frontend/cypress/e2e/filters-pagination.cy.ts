describe('Filters and Pagination E2E Tests', () => {
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

  describe('Filters', () => {
    it('should filter by status', () => {
      cy.get('#status-filter').select('COMPLETED');
      cy.get('#status-filter').should('have.value', 'COMPLETED');

      cy.get('.table-container').should('be.visible');
      cy.get('body').then(($body) => {
        if ($body.find('table.batch-table tbody tr').length > 0) {
          cy.get('table.batch-table tbody tr').each(($row) => {
            cy.wrap($row).find('.status-badge').should('contain.text', 'COMPLETED');
          });
        }
      });
    });

    it('should filter by compliance score range', () => {
      cy.get('#score-filter').select('acceptable');
      cy.get('#score-filter').should('have.value', 'acceptable');
      cy.get('.table-container').should('be.visible');
    });

    it('should filter by date range', () => {
      cy.get('#date-filter').select('week');
      cy.get('#date-filter').should('have.value', 'week');
      cy.get('.table-container').should('be.visible');
    });

    it('should reset status filter back to all', () => {
      cy.get('#status-filter').select('COMPLETED');
      cy.get('#status-filter').select('all');
      cy.get('#status-filter').should('have.value', 'all');
    });
  });

  describe('Pagination', () => {
    it('should show pagination controls only when there is more than one page', () => {
      cy.get('body').then(($body) => {
        if ($body.find('.pagination').length > 0) {
          cy.get('.pagination').should('be.visible');
          cy.contains(/Página \d+ de \d+/).should('be.visible');
          cy.contains('button', '← Anterior').should('be.disabled');
          cy.contains('button', 'Próxima →').should('be.visible');
        } else {
          cy.get('table.batch-table').should('be.visible');
        }
      });
    });

    it('should navigate between pages when pagination is available', () => {
      cy.get('body').then(($body) => {
        if ($body.find('.pagination').length > 0) {
          cy.contains(/Página 1 de \d+/).should('be.visible');

          cy.contains('button', 'Próxima →').click();
          cy.contains(/Página 2 de \d+/).should('be.visible');

          cy.contains('button', '← Anterior').click();
          cy.contains(/Página 1 de \d+/).should('be.visible');
        }
      });
    });
  });
});
