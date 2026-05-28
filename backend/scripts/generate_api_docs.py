#!/usr/bin/env python3
"""
Script to generate API documentation from FastAPI endpoints.

This script extracts endpoint information from FastAPI and generates
comprehensive API documentation in Markdown format.

Usage:
    python generate_api_docs.py --output docs/API.md
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any


def generate_api_docs(output_file: str = 'docs/API.md') -> None:
    """Generate API documentation from FastAPI endpoints.
    
    Args:
        output_file: Path to output documentation file
    """
    # This would typically import the FastAPI app and extract endpoints
    # For now, we create a template that can be filled in
    
    api_docs = """# API Documentation - BiotecPredict

## Overview

BiotecPredict REST API provides endpoints for uploading manufacturing data, 
retrieving batch information, and accessing compliance scores and risk predictions.

**Base URL**: `http://localhost:8000/api/v1`

---

## Authentication

Currently, the API uses basic authentication. Include credentials in request headers:

```
Authorization: Basic <base64-encoded-credentials>
```

---

## Endpoints

### Upload Batch Data

**POST** `/upload`

Upload a CSV file with manufacturing sensor data.

**Request**:
```http
POST /api/v1/upload HTTP/1.1
Content-Type: multipart/form-data

file: <CSV file>
```

**Response** (200 OK):
```json
{
  "batch_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "Batch received and queued for processing"
}
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "Invalid CSV format"
}
```

---

### List All Batches

**GET** `/batches`

Retrieve a list of all processed batches.

**Query Parameters**:
- `skip` (int, optional): Number of batches to skip (default: 0)
- `limit` (int, optional): Maximum number of batches to return (default: 100)
- `status` (string, optional): Filter by status (processing, completed, failed)

**Response** (200 OK):
```json
{
  "batches": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "batch_name": "Batch-001",
      "upload_date": "2026-05-24T10:30:00Z",
      "compliance_score": 85,
      "status": "completed"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

---

### Get Batch Details

**GET** `/batch/{batch_id}`

Retrieve detailed information about a specific batch.

**Path Parameters**:
- `batch_id` (string, required): UUID of the batch

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "batch_name": "Batch-001",
  "upload_date": "2026-05-24T10:30:00Z",
  "sensor_readings": [
    {
      "temperature": 37.5,
      "ph": 7.2,
      "dissolved_oxygen": 85.3,
      "pressure": 2.1,
      "agitator_speed": 250
    }
  ],
  "compliance_score": 85,
  "status": "completed"
}
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Batch not found"
}
```

---

### Get Compliance Score

**GET** `/compliance/{batch_id}`

Retrieve the manufacturing compliance score for a batch.

**Path Parameters**:
- `batch_id` (string, required): UUID of the batch

**Response** (200 OK):
```json
{
  "batch_id": "550e8400-e29b-41d4-a716-446655440000",
  "compliance_score": 85,
  "classification": "ACCEPTABLE",
  "details": {
    "temperature_score": 90,
    "ph_score": 85,
    "dissolved_oxygen_score": 80,
    "pressure_score": 85,
    "agitator_speed_score": 85
  }
}
```

---

### Get Risk Prediction

**GET** `/prediction/{batch_id}`

Retrieve the ML-based risk prediction for a batch.

**Path Parameters**:
- `batch_id` (string, required): UUID of the batch

**Response** (200 OK):
```json
{
  "batch_id": "550e8400-e29b-41d4-a716-446655440000",
  "risk_level": "LOW RISK",
  "confidence": 0.92,
  "model_version": "1.0.0",
  "prediction_timestamp": "2026-05-24T10:35:00Z"
}
```

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

---

## Rate Limiting

API requests are rate-limited to **100 requests per minute** per IP address.

Rate limit headers:
- `X-RateLimit-Limit`: Maximum requests per minute
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Unix timestamp when limit resets

---

## Examples

### Upload a batch using cURL

```bash
curl -X POST http://localhost:8000/api/v1/upload \\
  -F "file=@batch-data.csv"
```

### Get batch details using Python

```python
import requests

response = requests.get(
    'http://localhost:8000/api/v1/batch/550e8400-e29b-41d4-a716-446655440000'
)
batch = response.json()
print(f"Compliance Score: {batch['compliance_score']}")
```

### Get risk prediction using JavaScript

```javascript
fetch('http://localhost:8000/api/v1/prediction/550e8400-e29b-41d4-a716-446655440000')
  .then(response => response.json())
  .then(data => console.log(`Risk Level: ${data.risk_level}`));
```

---

## Swagger UI

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

**Last Updated**: 2026-05-24  
**API Version**: 1.0.0
"""
    
    # Create output directory if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write documentation
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(api_docs)
    
    print(f"✅ API documentation generated: {output_file}")


def main() -> None:
    """Main entry point."""
    output_file = 'docs/API.md'
    
    if len(sys.argv) > 2 and sys.argv[1] == '--output':
        output_file = sys.argv[2]
    
    generate_api_docs(output_file)


if __name__ == '__main__':
    main()
