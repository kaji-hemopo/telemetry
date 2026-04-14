# Airbnb Dashboard Data Integration Requirements

## Overview
This document outlines the technical requirements for integrating Felix's Airbnb research data into the dashboard system.

## Integration Timeline
- **Ready When:** Felix delivers data structure specifications (30-60 minutes)
- **Then:** Implement actual data integration
- **Priority:** MEDIUM-HIGH (Critical path but dependent on Felix)

## Current Status
✅ **Framework Ready:** Data ingestion system prepared
✅ **Placeholder Views:** Dashboard templates created  
✅ **Sample Data:** Test data matching expected format
✅ **Validation:** Data quality checks implemented
⏳ **Waiting:** Felix's actual data structure specifications

## Required Data Formats

### 1. Area Comparison Data
**Purpose:** Compare potential Airbnb locations (Shonan, Hakone, Shizuoka, Western Tokyo)

**Required Fields:**
```json
{
  "areas": [
    {
      "name": "string (required)",
      "region": "string (required)",
      "property_count": "integer (required)",
      "avg_price": "number (required)",
      "competition_score": "number (0-10 scale)",
      "regulation_score": "number (0-10 scale)",
      "notes": "string"
    }
  ]
}
```

**Display Requirements:**
- Table with sortable columns
- Color-coded scores (green=good, red=bad)
- Notes tooltip on hover
- Comparison visualization (bar charts)

### 2. Cost Breakdown Data
**Purpose:** Detailed cost analysis for property acquisition and operation

**Required Fields:**
```json
{
  "cost_breakdown": [
    {
      "category": "string (required)",
      "item": "string (required)",
      "estimated_cost": "number (required)",
      "frequency": "string (one_time|monthly|annual|per_guest)",
      "notes": "string"
    }
  ]
}
```

**Display Requirements:**
- Categorized cost tree
- Total cost calculations
- Monthly vs one-time cost separation
- Interactive cost adjustment sliders

### 3. Timeline Data
**Purpose:** Project timeline with dependencies and status

**Required Fields:**
```json
{
  "timeline": [
    {
      "phase": "string (required)",
      "task": "string (required)",
      "estimated_days": "integer (required)",
      "dependencies": "array of task IDs",
      "status": "string (pending|in_progress|completed|blocked)"
    }
  ]
}
```

**Display Requirements:**
- Gantt chart visualization
- Dependency arrows
- Status color coding
- Progress percentage

## Update Frequency Requirements

### Real-time Updates
- **Data Validation:** Immediate upon upload
- **Dashboard Refresh:** Within 1 minute of data change
- **Progress Tracking:** Real-time status updates

### Scheduled Updates
- **Research Data:** Hourly (when Felix completes research cycles)
- **Cost Updates:** Daily (as new cost information emerges)
- **Timeline Updates:** Real-time (as tasks progress)

### Manual Updates
- **Data Upload:** Via file upload interface
- **Manual Overrides:** For testing and adjustments
- **Data Corrections:** As needed

## Error Handling Requirements

### Data Validation Errors
- **Missing Fields:** Clear error messages specifying missing data
- **Type Mismatches:** Automatic type conversion where possible
- **Constraint Violations:** Highlight specific constraint failures
- **Data Inconsistencies:** Flag contradictory data points

### System Errors
- **File Upload Failures:** Retry mechanism with progress
- **Parsing Errors:** Detailed error logs with line numbers
- **Network Issues:** Offline mode with local storage
- **Integration Failures:** Fallback to last known good data

### User Experience Errors
- **Empty States:** Clear "no data" messages with guidance
- **Loading States:** Skeleton screens with progress indicators
- **Error States:** User-friendly error messages with recovery steps
- **Timeout Handling:** Automatic retry with user notification

## Technical Integration Points

### 1. Data Ingestion API
```
POST /api/data/upload
Content-Type: application/json
Body: Felix's research data JSON

Response: {
  "status": "success|error",
  "validation_results": {...},
  "dashboard_update": "scheduled|immediate"
}
```

### 2. Data Validation Webhook
```
POST /webhook/felix-data
Content-Type: application/json
Body: Research data update notification

Response: {
  "validation_started": true,
  "estimated_completion": "timestamp"
}
```

### 3. Dashboard Update Notification
```
GET /api/dashboard/status
Response: {
  "last_update": "timestamp",
  "next_update": "timestamp",
  "data_freshness": "minutes",
  "validation_status": "valid|warning|error"
}
```

## Testing Requirements

### Pre-Integration Testing
1. **Sample Data Test:** Verify dashboard displays sample data correctly
2. **Validation Test:** Ensure all validation rules work
3. **Error Handling Test:** Test all error scenarios
4. **Performance Test:** Verify dashboard loads within 2 seconds

### Integration Testing
1. **Data Flow Test:** End-to-end data ingestion → validation → display
2. **Update Test:** Verify real-time updates work
3. **Concurrency Test:** Multiple simultaneous updates
4. **Recovery Test:** System recovery after failures

### User Acceptance Testing
1. **Jackson Review:** Verify dashboard meets decision-making needs
2. **Felix Review:** Confirm data displays accurately
3. **Usability Test:** Intuitive navigation and understanding
4. **Mobile Test:** Responsive design on all devices

## Success Criteria

### Technical Success
- ✅ Data ingestion completes within 30 seconds
- ✅ Validation identifies 100% of data issues
- ✅ Dashboard updates within 1 minute of data change
- ✅ System handles 100+ concurrent data points
- ✅ Error recovery within 5 minutes

### User Success
- ✅ Jackson spends < 5 minutes understanding dashboard
- ✅ Data visualization leads to clear decisions
- ✅ No technical jargon or confusion
- ✅ Mobile access works perfectly
- ✅ Real-time updates are noticeable but not disruptive

### Business Success
- ✅ Dashboard accelerates property selection decision
- ✅ Cost analysis leads to accurate budgeting
- ✅ Timeline tracking prevents project delays
- ✅ Research coordination efficiency improved
- ✅ Manual data handling eliminated

## Next Steps

### Immediate (Waiting for Felix)
1. **Review Felix's data structure specifications**
2. **Adjust validation rules if needed**
3. **Update placeholder views to match actual data**
4. **Test with Felix's first data delivery**

### Upon Receiving Specifications
1. **Implement actual data parsing**
2. **Connect validation to real data**
3. **Update dashboard with live data**
4. **Test end-to-end integration**
5. **Deploy to production dashboard**

### Post-Integration
1. **Monitor system performance**
2. **Collect user feedback**
3. **Iterate on visualization improvements**
4. **Scale to additional research areas**

## Contact & Coordination
- **Saito:** Technical implementation & dashboard development
- **Felix:** Research data structure & delivery
- **Kaji:** Project coordination & timeline
- **Jackson:** User requirements & acceptance testing

---

**Last Updated:** 2026-03-21 22:41 JST  
**Status:** READY FOR FELIX'S DATA SPECIFICATIONS