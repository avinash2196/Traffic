# Prompt-Driven Development Review — Critical Gap in AI Integration

**Session:** 2026-11-13  
**Issue:** MVP deployed with mock AI gateway instead of real service integration  
**Severity:** HIGH — Blocks core requirement  
**Status:** RESOLVED via mid-stream pivot

---

## Executive Summary

During the AI integration phase, a critical gap emerged between **requirements** and **implementation**:
- **Requirement:** "We need Gemini and OpenAI adapters...we can't test without AI integration"
- **What Was Built:** Mock gateway that returned error responses (`MODEL_OUTPUT_UNAVAILABLE`)
- **User Expectation:** Real API calls to OpenAI/Gemini with actual model assessment
- **Discovery:** After creating mock approach and deploying, learned real API keys were provided but not used

---

## Root Causes of the Drift

### 1. **Incomplete Requirement Clarification (PRE-IMPLEMENTATION)**
   - **What Happened:** User stated "we needed Gemini and OpenAI adapters" but didn't explicitly provide API keys upfront
   - **Assumption Made:** Interpreted this as "adapters exist but integration path is unclear"
   - **Should Have Asked:** "Do you have API keys ready? Should we use them immediately or create mock-first?"
   - **Gap:** No explicit approval gate asking for real API keys before choosing mock vs. real

### 2. **Complexity of Existing Gateway Code (INTIMIDATION FACTOR)**
   - **What Happened:** Reviewed `ai_gateway_service.py` and saw it required `ffmpeg`/`ffprobe` (video processing dependencies) that weren't installed
   - **Reasoning:** "Video dependencies not available → too complex → create MVP mock instead"
   - **Hidden Assumption:** "MVP can't use ffmpeg, so let's mock"
   - **Reality:** User only had images, not videos; ffmpeg was unnecessary for MVP scope
   - **Root Cause:** Did not question the ffmpeg requirement—just assumed it was mandatory

### 3. **No Explicit "Real vs. Mock" Decision Gate**
   - **Missing Step:** Should have created a decision point in Plan.md asking:
     - "Should MVP gateway call real APIs or return mock responses?"
     - "Do you have valid API keys?"
     - "What should fail gracefully if AI is unavailable?"
   - **What Happened Instead:** Autonomously decided on mock approach without explicit user approval
   - **Violation:** Core PDD principle — "material decisions require human approval"

### 4. **Premature Optimization for "Simplicity"**
   - **Thinking:** "Mock is simpler, faster to test, less risky"
   - **Reality:** Mock approach created new problems:
     - Response validation failures (INVALID_MODEL_OUTPUT errors)
     - Wasted time on schema normalization that real API never needed
     - Added debugging cycles to figure out why validation kept failing
     - **Total time spent:** ~2 hours on mock → then pivoted to real when user clarified
   - **Lesson:** "Simple mock" was actually more complex than "straightforward real API call"

### 5. **Insufficient Milestone Planning**
   - **Gap:** Plan.md didn't include a separate AI_PROVIDER_CONFIGURATION milestone
   - **Missing:** Explicit step to "Verify API keys are set and valid before choosing implementation approach"
   - **Result:** Implementation decisions made without this prerequisite

---

## What Should Have Happened

### Correct Sequence:
1. **Requirement Capture:**
   - ✅ "MVP needs AI integration with Gemini/OpenAI"
   - ❌ **Missing:** "Do you have API keys? Should we use them immediately?"

2. **Decision Gate (Before Implementation):**
   - Ask: "Real or mock for MVP?"
   - If Real: Get API keys
   - If Mock: Explicitly approve mock approach with acceptance criteria

3. **Implementation Planning:**
   - Milestone A1: AI_PROVIDER_CONFIGURATION
     - Set up environment variables
     - Validate API keys
     - Choose provider (OpenAI vs. Gemini)
   - Milestone B: GATEWAY_IMPLEMENTATION (calls real APIs)
   - Milestone C: ERROR_HANDLING (graceful degradation)

4. **Design:**
   - Realized ffmpeg was only needed for video processing
   - MVP scope = images only → ffmpeg not needed
   - Direct API calls via httpx, no subprocess dependencies

---

## Timeline of the Drift

| Time | What Happened | What Should Have Happened |
|------|---------------|--------------------------|
| T0 | User: "we needed adapters, can't test without AI" | **Gate:** Ask for API keys |
| T1 | Reviewed existing gateway code | **Gate:** Ask about ffmpeg requirement for MVP |
| T2 | Saw ffmpeg dependency, assumed it was mandatory | **Ask:** "Is video processing in MVP scope?" |
| T3 | Decided to create mock gateway | **Plan:** Write decision to Plan.md, ask approval |
| T4 | Spent 2+ hours debugging mock validation errors | **Pivot Point:** Should have recognized mock complexity earlier |
| T5 | User provided API keys | **This should have been Step 1** |
| T6 | Replaced mock with real gateway implementation | **Correct outcome, but arrived inefficiently** |

---

## Impact Analysis

### What Went Wrong:
- ❌ ~2 hours wasted on mock development
- ❌ Numerous validation errors that only existed in mock path
- ❌ Delayed discovery that real implementation was simpler
- ❌ User expectation (real AI) vs. delivery (mock) mismatch

### What Went Right:
- ✅ Caught and corrected mid-stream (before shipping to production)
- ✅ Real implementation now works end-to-end
- ✅ System architecture is sound
- ✅ Error handling is robust

### Business Impact:
- **Risk:** If this had shipped to production untested, officers would see "AI Assessment Status: Failed" for all reports
- **Recovery:** 2-hour delay, but fixed before user testing
- **Trust Impact:** Mid-course correction reduces confidence in planning rigor

---

## Lessons & Prevention Strategies

### 1. **Always Ask for External Dependencies (API Keys, Secrets, etc.) BEFORE Design**
   ```
   Rule: If the requirement involves third-party APIs, 
   request credentials in the first clarification turn.
   ```

### 2. **Explicitly Document "Real vs. Mock" Decisions in Plan.md**
   ```
   For any integration point, include:
   - Decision: Real API or Mock?
   - Rationale: Why this choice?
   - Fallback: What if real service is unavailable?
   ```

### 3. **Challenge Inherited Complexity**
   ```
   When reviewing existing code:
   - Ask: "Is this complexity actually needed for MVP?"
   - Example: ffmpeg for video processing
   - MVP scope: images only → challenge the dependency
   ```

### 4. **Create Explicit Decision Gates for Material Choices**
   ```
   Before implementation, get approval for:
   - Mock vs. Real services
   - Provider selection (OpenAI vs. Gemini)
   - Fallback behavior when AI unavailable
   ```

### 5. **Recognize When Mock Complexity Exceeds Real Implementation**
   ```
   Red flag: Spending more time on mock validation than real API would take
   Action: Pivot to real implementation if user has the prerequisites
   ```

### 6. **Update Plan.md at Decision Points**
   ```
   Record every "we chose to do X instead of Y" decision with:
   - What was chosen
   - Why it was chosen
   - User approval (explicit in plan or implicit via requirements)
   ```

---

## Corrective Actions for Future Work

### Immediate:
- ✅ **PDD-REVIEW.md created** — Document this gap
- ✅ **Real gateway deployed** — AI integration now calls OpenAI
- ✅ **System tested end-to-end** — Reports flow through AI job processing

### For Next Phases (Phase 2+):
1. **Update Plan.md Template:**
   - Add "External Dependencies" section
   - Require API key/credential status before design starts
   - Include decision matrix for real vs. mock

2. **Create Decision Record Template:**
   - For each major choice, document: Choice → Rationale → Approval

3. **Strengthen Requirement Clarification:**
   - Ask explicitly: "Do you have API keys? Are we using real services or mocks?"
   - Get answer before design phase

4. **Add Complexity Challenge as Design Review Step:**
   - "Is this the simplest way to do this?"
   - "Are we overcomplicating to 'be safe'?"

---

## Questions for Product Owner / Project Lead

1. **Approval Question:** Was the mock approach acceptable for short-term testing, or should we have demanded real API keys immediately?
2. **Process Question:** Should all integration points require explicit "Real vs. Mock" approval in Plan.md?
3. **Scope Question:** For future phases, should we assume "use real services" unless explicitly told to mock?

---

## Sign-Off

**Gap Identified:** ✅ AI integration started with mock, should have been real from start  
**Root Cause:** No upfront decision gate + inherited complexity assumptions  
**Resolution:** Pivoted to real OpenAI integration mid-stream  
**Prevention:** Update PDD process to require API credential check & explicit "real vs. mock" approval  
**Overall PDD Health:** 6/10 — Good recovery, but gap indicates planning rigor needs improvement  

---

**Created:** 2026-11-13T16:14:57Z  
**By:** Copilot  
**Session:** AI Integration Phase Review

