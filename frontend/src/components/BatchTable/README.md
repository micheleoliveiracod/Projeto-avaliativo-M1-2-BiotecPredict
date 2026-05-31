# BatchTable Component

## Overview

The `BatchTable` component displays a comprehensive table of processed batches with advanced filtering, sorting, and pagination capabilities. It provides a user-friendly interface for viewing batch history with compliance scores and risk levels.

## Features

- **Batch Display**: Shows all processed batches in a structured table format
- **Columns**: ID, Upload Date, Compliance Score, Risk Level, Status
- **Filtering**: Filter by date range, status, and compliance score range
- **Pagination**: Navigate through batches with configurable items per page (5, 10, 20, 50)
- **Responsive Design**: Fully responsive layout that works on mobile, tablet, and desktop
- **Accessibility**: Keyboard navigation support and proper ARIA attributes
- **Localization**: Portuguese (pt-BR) formatting for dates and numbers

## Installation

The component is already installed in the project. Import it from the components directory:

```tsx
import { BatchTable } from '@/components/BatchTable'
// or
import BatchTable from '@/components/BatchTable/BatchTable'
```

## Usage

### Basic Example

```tsx
import React, { useState, useEffect } from 'react'
import { BatchTable, Batch } from '@/components/BatchTable'

export function MyComponent() {
  const [batches, setBatches] = useState<Batch[]>([])

  useEffect(() => {
    // Fetch batches from API
    fetchBatches()
  }, [])

  const fetchBatches = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/batches')
      const data = await response.json()
      setBatches(data)
    } catch (error) {
      console.error('Error fetching batches:', error)
    }
  }

  const handleRowClick = (batch: Batch) => {
    console.log('Clicked batch:', batch)
    // Navigate to batch details or perform other actions
  }

  return (
    <BatchTable 
      batches={batches} 
      onRowClick={handleRowClick}
    />
  )
}
```

### With Custom Styling

```tsx
<BatchTable 
  batches={batches} 
  onRowClick={handleRowClick}
  className="custom-class"
/>
```

## Props

### BatchTableProps

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `batches` | `Batch[]` | Yes | Array of batch objects to display |
| `onRowClick` | `(batch: Batch) => void` | No | Callback function when a row is clicked |
| `className` | `string` | No | Additional CSS class names for the container |

### Batch Interface

```typescript
interface Batch {
  id: string                                    // Unique batch identifier
  upload_date: string                           // ISO 8601 date string
  compliance_score: number                      // Score from 0-100
  risk_level: 'LOW RISK' | 'MEDIUM RISK' | 'HIGH RISK'  // Risk classification
  status: 'ACCEPTABLE' | 'WARNING' | 'CRITICAL'         // Status classification
}
```

## Features in Detail

### Filtering

The component provides multiple filter options:

1. **Date Range**: Filter batches by upload date (from and to)
2. **Status**: Filter by compliance status (ACCEPTABLE, WARNING, CRITICAL)
3. **Score Range**: Filter by compliance score (minimum and maximum)

All filters work together and can be combined. The "Clear Filters" button resets all filters at once.

### Pagination

- **Default**: 10 items per page
- **Options**: 5, 10, 20, or 50 items per page
- **Navigation**: First, Previous, Next, Last page buttons
- **Info**: Current page and total pages displayed

### Data Formatting

- **Dates**: Formatted in pt-BR locale (DD/MM/YYYY HH:mm:ss)
- **Numbers**: Formatted with 2 decimal places using pt-BR locale
- **Risk Levels**: Color-coded (Green for LOW, Yellow for MEDIUM, Red for HIGH)
- **Status**: Color-coded (Green for ACCEPTABLE, Yellow for WARNING, Red for CRITICAL)

### Accessibility

- Keyboard navigation support (Enter/Space to select rows)
- Proper ARIA attributes and roles
- Semantic HTML structure
- Focus management
- Screen reader friendly

## Styling

The component uses CSS Modules for styling. The main stylesheet is `BatchTable.module.css`.

### CSS Classes

- `.container`: Main container
- `.filtersSection`: Filters area
- `.tableWrapper`: Table wrapper with scroll
- `.table`: Main table element
- `.tableRow`: Table row (clickable)
- `.paginationSection`: Pagination controls

### Responsive Breakpoints

- **Desktop**: Full layout with all features
- **Tablet (≤768px)**: Adjusted spacing and font sizes
- **Mobile (≤480px)**: Compact layout with smaller fonts and buttons

## Testing

The component includes comprehensive tests using Vitest and React Testing Library.

### Running Tests

```bash
# Run all tests
npm test

# Run only BatchTable tests
npm test -- BatchTable.test.tsx

# Run with coverage
npm test:coverage
```

### Test Coverage

The component has ≥80% code coverage including:

- Rendering tests
- Filter functionality tests
- Pagination tests
- Data formatting tests
- Accessibility tests
- Edge case tests
- Combined filter and pagination tests

## Performance Considerations

- Uses `useMemo` for filtering and pagination to prevent unnecessary recalculations
- Uses `useCallback` for event handlers to prevent unnecessary re-renders
- Efficient date and number formatting
- Optimized CSS with minimal reflows

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: iOS Safari 12+, Chrome Android 90+

## Troubleshooting

### Batches not displaying

1. Check that the `batches` prop is correctly passed
2. Verify the batch data structure matches the `Batch` interface
3. Check browser console for errors

### Filters not working

1. Ensure filter values are valid (dates in YYYY-MM-DD format)
2. Check that batch data has the correct fields
3. Verify filter logic in the component

### Pagination issues

1. Check that `itemsPerPage` is a valid number
2. Verify that `currentPage` is within valid range
3. Ensure batches array is not empty

## Examples

### Complete Dashboard Integration

```tsx
import React, { useState, useEffect } from 'react'
import { BatchTable, Batch } from '@/components/BatchTable'
import axios from 'axios'

export function Dashboard() {
  const [batches, setBatches] = useState<Batch[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchBatches()
  }, [])

  const fetchBatches = async () => {
    try {
      setLoading(true)
      const response = await axios.get('http://localhost:8000/api/v1/batches')
      setBatches(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to fetch batches')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleRowClick = (batch: Batch) => {
    // Navigate to batch details
    window.location.href = `/batch/${batch.id}`
  }

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div className="dashboard">
      <h1>Batch History</h1>
      <BatchTable 
        batches={batches} 
        onRowClick={handleRowClick}
      />
    </div>
  )
}
```

### With Real-time Updates

```tsx
import React, { useState, useEffect } from 'react'
import { BatchTable, Batch } from '@/components/BatchTable'

export function LiveBatchTable() {
  const [batches, setBatches] = useState<Batch[]>([])

  useEffect(() => {
    // Initial fetch
    fetchBatches()

    // Poll for updates every 5 seconds
    const interval = setInterval(fetchBatches, 5000)

    return () => clearInterval(interval)
  }, [])

  const fetchBatches = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/batches')
      const data = await response.json()
      setBatches(data)
    } catch (error) {
      console.error('Error fetching batches:', error)
    }
  }

  return <BatchTable batches={batches} />
}
```

## Related Components

- `Dashboard`: Main dashboard component that uses BatchTable
- `ComplianceScoreCard`: Displays compliance score details
- `RiskPredictionCard`: Displays risk prediction details
- `SensorCharts`: Displays sensor data visualizations

## Contributing

When modifying this component:

1. Update tests to cover new functionality
2. Maintain ≥80% code coverage
3. Follow the existing code style
4. Update this README with any new features
5. Test on multiple screen sizes
6. Ensure accessibility compliance

## License

This component is part of the BiotecPredict project and follows the project's license.

---

**Version**: 1.0.0  
**Last Updated**: 31/05/2026  
**Status**: ✅ Complete and Tested
