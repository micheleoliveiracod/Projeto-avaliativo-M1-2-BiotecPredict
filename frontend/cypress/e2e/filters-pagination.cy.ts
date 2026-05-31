describe('Filters and Pagination E2E Tests', () => {
  beforeEach(() => {
    cy.visit('/dashboard');
  });

  describe('Filters', () => {
    it('should filter by date range', () => {
      cy.get('[data-testid="filter-start-date"]').type('2026-05-01');
      cy.get('[data-testid="filter-end-date"]').type('2026-05-31');
      cy.get('[data-testid="filter-button"]').click();
      cy.get('[data-testid="batch-table"]').should('be.visible');
    });

    it('should filter by status', () => {
      cy.get('[data-testid="filter-status"]').select('ACCEPTABLE');
      cy.get('[data-testid="filter-button"]').click();
      cy.get('table tbody tr').each(($row) => {
        cy.wrap($row).contains('ACCEPTABLE').should('be.visible');
      });
    });

    it('should filter by compliance score range', () => {
      cy.get('[data-testid="filter-min-score"]').type('80');
      cy.get('[data-testid="filter-max-score"]').type('100');
      cy.get('[data-testid="filter-button"]').click();
      cy.get('[data-testid="batch-table"]').should('be.visible');
    });

    it('should clear filters', () => {
      cy.get('[data-testid="filter-start-date"]').type('2026-05-01');
      cy.get('[data-testid="filter-clear"]').click();
      cy.get('[data-testid="filter-start-date"]').should('have.value', '');
    });
  });

  describe('Pagination', () => {
    it('should display pagination controls', () => {
      cy.get('[data-testid="pagination"]').should('be.visible');
      cy.get('[data-testid="pagination-prev"]').should('be.visible');
      cy.get('[data-testid="pagination-next"]').should('be.visible');
    });

    it('should navigate to next page', () => {
      cy.get('[data-testid="pagination-next"]').click();
      cy.get('[data-testid="current-page"]').should('contain', '2');
    });

    it('should navigate to previous page', () => {
      cy.get('[data-testid="pagination-next"]').click();
      cy.get('[data-testid="pagination-prev"]').click();
      cy.get('[data-testid="current-page"]').should('contain', '1');
    });

    it('should change items per page', () => {
      cy.get('[data-testid="items-per-page"]').select('20');
      cy.get('table tbody tr').should('have.length.lessThan', 21);
    });

    it('should display page info', () => {
      cy.get('[data-testid="page-info"]').should('contain', /Página \d+ de \d+/);
    });
  });

  describe('Polling', () => {
    it('should display polling interval selector', () => {
      cy.get('[data-testid="polling-interval"]').should('be.visible');
    });

    it('should change polling interval', () => {
      cy.get('[data-testid="polling-interval"]').select('10s');
      cy.get('[data-testid="polling-interval"]').should('have.value', '10000');
    });

    it('should display last update timestamp', () => {
      cy.get('[data-testid="last-update"]').should('be.visible');
      cy.get('[data-testid="last-update"]').should('contain', /\d{2}:\d{2}:\d{2}/);
    });

    it('should manually refresh data', () => {
      cy.get('[data-testid="refresh-button"]').click();
      cy.get('[data-testid="loading-spinner"]').should('be.visible');
      cy.get('[data-testid="loading-spinner"]').should('not.exist');
    });
  });
});
