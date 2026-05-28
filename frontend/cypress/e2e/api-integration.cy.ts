describe('API Integration E2E Tests', () => {
  const API_BASE_URL = 'http://localhost:8000/api/v1';

  it('should upload batch via API', () => {
    const csvContent = `temperature,ph,dissolved_oxygen,pressure,agitator_speed
37.5,7.2,85.3,2.1,250
38.0,7.1,84.5,2.2,255`;

    cy.request({
      method: 'POST',
      url: `${API_BASE_URL}/upload`,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: {
        file: csvContent,
      },
    }).then((response) => {
      expect(response.status).to.equal(200);
      expect(response.body).to.have.property('batch_id');
    });
  });

  it('should retrieve batches list', () => {
    cy.request({
      method: 'GET',
      url: `${API_BASE_URL}/batches`,
    }).then((response) => {
      expect(response.status).to.equal(200);
      expect(response.body).to.have.property('batches');
      expect(response.body.batches).to.be.an('array');
    });
  });

  it('should retrieve batch details', () => {
    cy.request({
      method: 'GET',
      url: `${API_BASE_URL}/batches`,
    }).then((response) => {
      const batchId = response.body.batches[0]?.id;
      
      if (batchId) {
        cy.request({
          method: 'GET',
          url: `${API_BASE_URL}/batch/${batchId}`,
        }).then((detailResponse) => {
          expect(detailResponse.status).to.equal(200);
          expect(detailResponse.body).to.have.property('id');
          expect(detailResponse.body).to.have.property('sensor_readings');
        });
      }
    });
  });

  it('should retrieve compliance score', () => {
    cy.request({
      method: 'GET',
      url: `${API_BASE_URL}/batches`,
    }).then((response) => {
      const batchId = response.body.batches[0]?.id;
      
      if (batchId) {
        cy.request({
          method: 'GET',
          url: `${API_BASE_URL}/compliance/${batchId}`,
        }).then((complianceResponse) => {
          expect(complianceResponse.status).to.equal(200);
          expect(complianceResponse.body).to.have.property('compliance_score');
          expect(complianceResponse.body).to.have.property('classification');
        });
      }
    });
  });

  it('should retrieve risk prediction', () => {
    cy.request({
      method: 'GET',
      url: `${API_BASE_URL}/batches`,
    }).then((response) => {
      const batchId = response.body.batches[0]?.id;
      
      if (batchId) {
        cy.request({
          method: 'GET',
          url: `${API_BASE_URL}/prediction/${batchId}`,
        }).then((predictionResponse) => {
          expect(predictionResponse.status).to.equal(200);
          expect(predictionResponse.body).to.have.property('risk_level');
          expect(predictionResponse.body).to.have.property('confidence');
        });
      }
    });
  });

  it('should handle invalid batch ID gracefully', () => {
    cy.request({
      method: 'GET',
      url: `${API_BASE_URL}/batch/invalid-id`,
      failOnStatusCode: false,
    }).then((response) => {
      expect(response.status).to.equal(404);
    });
  });
});
