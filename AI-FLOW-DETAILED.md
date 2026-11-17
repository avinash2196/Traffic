# RoadWatch AI Processing Flow - Detailed Explanation

## Overview

When a citizen submits a traffic violation report with a photo, the system makes **2 AI calls** to analyze and confirm violations:

1. **CALL 1: `/v1/assessments`** - Main AI analysis (what does the image show?)
2. **CALL 2: `/v1/breakdown`** - Violation confirmation (which specific violations are present?)

---

## CALL 1: `/v1/assessments` - Main Analysis

### Who Calls It?
- **ai-worker** (background service) calls **ai-gateway** after finding a pending job

### What Gets Sent?

```json
POST http://127.0.0.1:9004/v1/assessments

{
  "correlation_id": "60687add636846eb",
  "attempt_id": "60687add636846eb", 
  "attempt_number": 1,
  "evidence_revision": 1,
  "selection": {
    "provider": "openai",
    "request_profile_version": "1.0",
    "media_profile_version": "1.0"
  },
  "prompt": {
    "text": "Assess traffic violation: helmet by vehicle MH01AB1234 at Mumbai",
    "version": "1.0",
    "policy_version": "1.0",
    "legal_reference_version": "1.0"
  },
  "evidence": [
    {
      "media_id": "abc123def456",
      "mime_type": "image/jpeg",
      "data_base64": "iVBORw0KGgo...AAAA" (actual JPEG bytes, base64 encoded)
    }
  ]
}
```

### What Happens Inside ai-gateway?

1. **Parse Request**
   - Extract image from base64
   - Extract violation type ("helmet")
   - Extract vehicle info ("MH01AB1234")

2. **Call OpenAI**
   ```
   POST https://api.openai.com/v1/chat/completions
   
   Model: gpt-4o-mini
   Temperature: 0.3 (consistent, not creative)
   Max Tokens: 4096
   
   System Prompt: Detailed instructions about traffic law assessment
   User Input: Image + Context (violation type, vehicle, location)
   ```

3. **Receive OpenAI Response**
   ```json
   {
     "type": "object",
     "properties": {
       "relevance": "High",
       "violation_confidence": 0.85,
       "relevance_confidence": 0.9,
       "recommendation": "Issue warning for not wearing helmets...",
       "explanation": "The image shows multiple individuals on a two-wheeler without helmets...",
       "observations": ["Two riders are not wearing helmets"],
       "attachment_relevance": ["Helmet usage is critical..."],
       "rule_notes": ["Most jurisdictions require helmets..."]
     }
   }
   ```

4. **Transform to Strict Schema**
   - OpenAI returns simple strings/arrays
   - Need to convert to strict schema with objects containing media_id, start_ms, end_ms
   - Add MVA reference IDs to rule_notes
   - Normalize confidence scores (0-100 scale)

5. **Validate**
   - Check all required fields present
   - Verify schema matches assessment_policy
   - If validation fails → 502 error
   - If valid → continue

6. **Return 200 OK**
   ```json
   {
     "correlation_id": "60687add636846eb",
     "assessment": {
       "relevance": "relevant",
       "violation_confidence": 85,
       "relevance_confidence": 90,
       "recommendation": "Issue warning...",
       "explanation": "The image shows riders without helmets...",
       "observations": [
         {
           "media_id": "abc123def456",
           "text": "Riders are not wearing helmets",
           "start_ms": null,
           "end_ms": null
         }
       ],
       "attachment_relevance": [
         {
           "media_id": "abc123def456",
           "relevance": "relevant",
           "reason": "Helmet violation clearly visible"
         }
       ],
       "rule_notes": [
         {
           "reference_id": "MVA-129-2019",
           "applicability": "potentially-applicable",
           "note": "Helmet use is mandatory...",
           "section": "Section 129",
           "title": "Motor Vehicles Act 1988",
           "url": "https://www.indiacode.nic.in/..."
         }
       ],
       "limitations": [
         "Officer review required for final determination",
         "AI confidence scores are uncalibrated estimates"
       ]
     },
     "provider": "openai",
     "model": "gpt-4o-mini",
     "processing_ms": 5922
   }
   ```

### What Does Call 1 Provide?

✅ **Full context** - what OpenAI saw in the image  
✅ **Confidence scores** - how certain about violations (0-100)  
✅ **Legal references** - MVA sections that apply  
✅ **Detailed explanation** - what specifically was observed  
✅ **Observations** - breakdown by media file  
✅ **Limitations** - what AI couldn't determine  

### Processing Time
- ~6 seconds (5922ms in the example)
- OpenAI API call: ~5-6 seconds
- Schema validation: ~20ms

---

## CALL 2: `/v1/breakdown` - Confirm Specific Violations

### Who Calls It?
- **ai-worker** (after Call 1 succeeds) calls **ai-gateway**

### What Gets Sent?

```json
POST http://127.0.0.1:9004/v1/breakdown

{
  "assessment": {
    "relevance": "relevant",
    "violation_confidence": 85,
    "relevance_confidence": 90,
    "recommendation": "Issue warning...",
    "explanation": "The image shows riders without helmets...",
    "observations": [...],           ← REUSES from Call 1
    "attachment_relevance": [...],   ← REUSES from Call 1
    "rule_notes": [...]              ← REUSES from Call 1
  },
  "evidence": [
    {
      "media_id": "abc123def456",
      "mime_type": "image/jpeg",
      "data_base64": "iVBORw0KGgo..." ← SAME IMAGE as Call 1
    }
  ]
}
```

### What Happens Inside ai-gateway?

1. **Build Confirmation Prompt**
   ```
   Based on this assessment: [Call 1 results]
   
   Confirm which violations are present (yes/no):
   1. no_helmet - Are riders NOT wearing helmets?
   2. triple_riding - Are there MORE than 2 people on vehicle?
   3. red_light - Is vehicle crossing at RED signal?
   
   Return ONLY valid JSON: {"violations": {"no_helmet": true/false, ...}}
   ```

2. **Call OpenAI** (simpler than Call 1)
   ```
   Model: gpt-4o-mini (same as Call 1)
   Temperature: 0.2 (MORE deterministic than Call 1's 0.3)
   Max Tokens: 500 (much smaller than Call 1's 4096)
   
   Input: Confirmation prompt above
   ```

3. **Receive OpenAI Response**
   ```json
   {
     "violations": {
       "no_helmet": true,
       "triple_riding": false,
       "red_light": false
     }
   }
   ```

4. **Parse JSON**
   - Extract boolean flags
   - Validate format

5. **Return 200 OK**
   ```json
   {
     "correlation_id": "60687add636846eb",
     "breakdown": {
       "violations": {
         "no_helmet": true,         ← Confirmed: missing helmets
         "triple_riding": false,    ← Confirmed: only 2 people
         "red_light": false         ← Confirmed: not at red light
       }
     },
     "provider": "openai",
     "model": "gpt-4o-mini",
     "processing_ms": 1245
   }
   ```

### What Does Call 2 Provide?

✅ **Actionable booleans** - yes/no for each violation type  
✅ **Faster** - ~1.2 seconds vs 6 seconds  
✅ **Cheaper** - fewer tokens (simple confirmation)  
✅ **Consistent** - based on Call 1's analysis, not independent  
✅ **Parseable** - structured output, easy to store in DB  

### Processing Time
- ~1.2 seconds (1245ms in the example)
- Much faster because:
  - Smaller prompt
  - Lower temperature (0.2 vs 0.3)
  - Only asking for boolean confirmation
  - OpenAI doesn't need to do deep analysis

---

## Combining Both Responses

After both calls succeed, **ai-worker combines them**:

```json
{
  "assessment": {
    "relevance": "relevant",
    "violation_confidence": 85,
    "recommendation": "Issue warning...",
    "explanation": "The image shows riders without helmets...",
    "observations": [...],
    "attachment_relevance": [...],
    "rule_notes": [...]
  },
  "breakdown": {
    "violations": {
      "no_helmet": true,
      "triple_riding": false,
      "red_light": false
    }
  },
  "correlation_id": "60687add636846eb",
  "assessment_time_ms": 5922,
  "breakdown_time_ms": 1245
}
```

This combined result is **saved in the database** (ai_jobs table with state='success').

---

## What Officer Sees

Officer opens portal and sees:

```
Report: MH01AB1234 - Mumbai - Helmet Violation
Status: AI Review Complete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Relevance: RELEVANT (90% confidence)
Violation Confidence: 85%

Explanation:
  "The image shows riders without helmets on a two-wheeler,
   which violates traffic safety regulations."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONFIRMED VIOLATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ No Helmet: YES (riders not wearing helmets)
✗ Triple Riding: NO (only 2 people on vehicle)
✗ Red Light: NO (not crossing at red signal)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEGAL REFERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MVA-129-2019 (Section 129): 
  "Helmet use is mandatory for all riders and passengers on two-wheelers."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OFFICER DECISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ Approve ]  [ Reject ]  [ Need More Review ]

If approved: Award 2 provisional points (motorcycle helmet violation)
```

---

## Why Two Calls?

| Aspect | Call 1 | Call 2 | Reason |
|--------|--------|--------|--------|
| **Purpose** | Deep analysis | Quick confirmation | Call 1 provides context, Call 2 confirms specifics |
| **Input** | Image only | Assessment + Image | Reuse Call 1's analysis to avoid repetition |
| **Output** | Detailed JSON | Boolean flags | Easier to parse and store |
| **Processing Time** | ~6 seconds | ~1.2 seconds | Call 2 is simpler |
| **Token Cost** | Higher | Lower | Call 2 uses fewer tokens |
| **Complexity** | Complex schema | Simple format | Different output requirements |
| **Accuracy** | Foundation | Based on Call 1 | Call 2 confirms, doesn't create new analysis |

---

## Error Handling

### If Call 1 Fails
- Returns 502 Bad Gateway
- ai-worker marks job as "failed"
- Officer sees: "AI assessment failed - requires manual review"
- Officer can still make decision based on image

### If Call 2 Fails
- Call 1 response is still saved
- Officer sees: "Full AI analysis available, violation breakdown unavailable"
- Officer has enough info to make decision

### If Network Timeout
- ai-worker retries up to 3 times
- Waits 10 seconds between retries
- After 3 failures, marks as failed

---

## Database Storage

Results are stored in **ai_jobs** table:

```sql
INSERT INTO ai_jobs (
  id,
  report_id,
  state,
  result_json,
  attempt_count,
  created_at,
  updated_at
) VALUES (
  'correlation_id_here',
  'report_id_here',
  'success',
  '{"assessment": {...}, "breakdown": {...}}',
  1,
  '2026-11-17T04:40:00Z',
  '2026-11-17T04:40:07Z'
);
```

Officer API retrieves this when querying report details:
```python
GET /api/authority/reports/{report_id}

Response includes:
{
  "id": "report_id",
  "ai": {
    "state": "success",
    "assessment": {...},
    "breakdown": {...}
  }
}
```

---

## Summary

```
Citizen submits photo
        ↓
ai-worker picks up job
        ↓
CALL 1: Send to OpenAI → Get full analysis (~6 sec)
        ↓
CALL 2: Ask OpenAI to confirm violations (~1.2 sec)
        ↓
Save combined result to database
        ↓
Officer sees analysis + confirmed violations
        ↓
Officer makes decision: Approve / Reject / Review
```

**Total time: ~7-8 seconds from submission to ready for review**
