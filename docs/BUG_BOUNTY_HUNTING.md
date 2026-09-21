# Bug Bounty Hunting Guide

## Overview

The VAPT engine now includes **intelligent bug bounty hunting** powered by:
- Claude AI reasoning about vulnerabilities
- Real bug bounty data from YesWeHack
- Systematic hunting methodology
- ROI-focused vulnerability prioritization

Hunt for high-impact vulnerabilities worth **$1000-$5000+** systematically.

---

## Key Features

### 1. Intelligent Bug Hunting
✓ Analyzes target technology stack  
✓ Identifies likely vulnerabilities  
✓ Prioritizes by bounty potential  
✓ Systematic hunting workflow  
✓ Generates detailed hunting reports  

### 2. YesWeHack Data Integration
✓ 10+ real bug bounty report examples  
✓ Common vulnerability patterns  
✓ Discovery techniques  
✓ Exploitation methods  
✓ Bounty value data  

### 3. Claude-Powered Analysis
✓ Recommends high-ROI targets  
✓ Provides exploitation guidance  
✓ Chains vulnerabilities together  
✓ Identifies business impact  
✓ Suggests escalation paths  

---

## Getting Started

### Quick Hunt

```bash
export ANTHROPIC_API_KEY="sk-ant-..."

vapt bug-bounty hunt \
    --client "Your Client" \
    --target "https://app.example.com"
```

**What Happens:**
1. Claude analyzes target technology
2. Reviews YesWeHack bug data
3. Prioritizes hunting targets by ROI
4. Hunts systematically for each
5. Generates report with findings

### Explore Bug Bounty Data

```bash
# See top findings worth hunting for
vapt bug-bounty top-findings --min-bounty 2000

# Get checklist for your tech stack
vapt bug-bounty tech-checklist --tech-stack "React" --tech-stack "Node.js"

# Get detailed exploitation guide
vapt bug-bounty exploitation-guide --type "IDOR"

# View common patterns in bug bounties
vapt bug-bounty vulnerability-patterns
```

---

## The Hunting Workflow

### Phase 1: Target Analysis

Claude analyzes:
- Frontend framework
- Backend technology
- Database type
- APIs and services
- Infrastructure

**Output:** Technology stack with risk profile

### Phase 2: Hunting Plan

Based on technology + bug bounty data, Claude identifies:
- High-probability vulnerabilities
- Quick wins (easy to find)
- High-value targets ($1000+)
- Escalation opportunities
- Chaining possibilities

**Output:** Prioritized hunting targets ranked by ROI

### Phase 3: Systematic Hunting

For each target vulnerability:
1. Generate specific discovery steps
2. Identify exploitation techniques
3. Test against target
4. Verify if vulnerable
5. Document findings

**Output:** Confirmed vulnerabilities with evidence

### Phase 4: Impact Assessment

Claude evaluates:
- Business impact
- Data exposure
- System compromise
- Privilege escalation
- Lateral movement

**Output:** Severity assessment and remediation

### Phase 5: Reporting

Generate comprehensive report with:
- Executive summary
- Detailed findings
- Hunting efficiency metrics
- Bounty analysis
- Next steps

**Output:** Professional hunting report

---

## Real-World Vulnerabilities

The system knows about these high-impact findings commonly found in bug bounties:

### 1. IDOR (Insecure Direct Object References)
**Bounty:** $2,000  
**Severity:** High  
**Difficulty:** Low  
**ROI:** $400/hour

Discovery:
```
1. Identify user ID parameter: /api/users/{id}
2. Change ID while logged in
3. Check if you access other users' data
```

### 2. JWT Authentication Bypass
**Bounty:** $3,000  
**Severity:** High  
**Difficulty:** Medium  
**ROI:** $300/hour

Discovery:
```
1. Extract hardcoded secret from JavaScript
2. Use jwt.io to decode token
3. Modify claims (role: 'admin')
4. Re-encode and use
```

### 3. SQL Injection
**Bounty:** $5,000  
**Severity:** Critical  
**Difficulty:** Medium  
**ROI:** $500/hour

Discovery:
```
1. Test search parameter with: ' OR '1'='1
2. Look for database errors
3. Use UNION-based injection
4. Dump user database
```

### 4. Privilege Escalation (Client-Side Check)
**Bounty:** $2,500  
**Severity:** High  
**Difficulty:** Low  
**ROI:** $500/hour

Discovery:
```
1. Find admin endpoint in code
2. Call endpoint as regular user
3. Observe no server-side check
4. Access admin functions
```

### 5. AWS S3 Bucket Exposure
**Bounty:** $4,000  
**Severity:** High  
**Difficulty:** Low  
**ROI:** $800/hour

Discovery:
```
1. Find bucket name in JavaScript
2. Test: https://bucket.s3.amazonaws.com/
3. List bucket contents
4. Download sensitive files
```

### 6. CORS Misconfiguration
**Bounty:** $3,000  
**Severity:** High  
**Difficulty:** Low  
**ROI:** $600/hour

Discovery:
```
1. Check CORS headers on API
2. Look for: Access-Control-Allow-Origin: *
3. Create malicious page
4. Steal data when victim visits
```

### 7. API Rate Limiting Bypass
**Bounty:** $1,500  
**Severity:** Medium  
**Difficulty:** Low  
**ROI:** $300/hour

Discovery:
```
1. Send rapid login requests
2. No rate limiting or lockout
3. Brute force weak passwords
4. Gain account access
```

### 8. Reflected XSS
**Bounty:** $1,000  
**Severity:** Medium  
**Difficulty:** Low  
**ROI:** $200/hour

Discovery:
```
1. Find error parameter: ?error=value
2. Inject: <img src=x onerror=alert('XSS')>
3. Create cookie-stealing payload
4. Steal admin sessions
```

---

## Usage Examples

### Example 1: Hunt for IDOR

```bash
vapt bug-bounty hunt \
    --client "Acme Corp" \
    --target "https://app.acme.com"

# Claude will recommend testing:
# - /api/users/{id} → IDOR candidate
# - /api/orders/{id} → Check for IDOR
# - /api/profile → Check authorization
# etc.
```

Claude provides:
- Exact parameters to test
- Exploitation steps
- How to verify
- Expected bounty ($2,000)

### Example 2: Tech Stack Analysis

```bash
vapt bug-bounty tech-checklist \
    --tech-stack "React" \
    --tech-stack "Node.js" \
    --tech-stack "MongoDB"

# Gets testing checklist for this specific stack
# Shows top 5 vulnerabilities commonly found in React+Node+MongoDB:
# 1. Client-side authorization bypass
# 2. CORS misconfiguration  
# 3. Weak password hashing
# 4. NoSQL injection
# 5. JWT validation issues
```

### Example 3: Exploitation Guide

```bash
vapt bug-bounty exploitation-guide --type "IDOR"

# Shows:
# - What IDOR is
# - How to discover it
# - Step-by-step exploitation
# - Proof of concept
# - Remediation steps
# - Similar findings from bug bounties
```

### Example 4: Top Findings

```bash
vapt bug-bounty top-findings --min-bounty 2000

# Shows vulnerabilities worth $2000+
# Sorted by bounty value or frequency
# Includes discovery technique for each
```

---

## Hunting Strategy

### High-ROI Targets (Focus Here)

**Best effort/reward ratio:**

1. **IDOR** ($2,000, easy to find)
   - Test every ID parameter
   - Check authorization
   - Dump all records

2. **Client-Side Authorization** ($2,500, very easy)
   - Find admin endpoint
   - Call as regular user
   - No server check = instant win

3. **Exposed S3 Bucket** ($4,000, quick)
   - Search JS for bucket name
   - Test public access
   - Download files

4. **JWT Secret in Code** ($3,000, medium)
   - Extract from JS
   - Forge tokens
   - Become admin

### Medium-Term Targets

- SQL Injection ($5,000, medium effort)
- CORS Bypass ($3,000, medium effort)
- Weak Rate Limiting ($1,500, easy)

### Long-Term Investigations

- Complex privilege escalation chains
- Business logic flaws
- Race conditions
- API abuse scenarios

---

## Maximizing Bounty Value

### 1. Prioritize by ROI
```
ROI = Bounty / (Effort Hours)

IDOR: $2,000 / 0.5 hours = $4,000/hour ← Hunt this first
JWT Bypass: $3,000 / 1 hour = $3,000/hour
SQL Injection: $5,000 / 3 hours = $1,666/hour
```

### 2. Chain Vulnerabilities

```
Discovery:
→ IDOR in /api/users/{id} (exposes emails)
→ Email-based password reset
→ Extract reset token from email parameter
→ Reset admin password
→ Login as admin
→ Access sensitive data

Total impact: Low IDOR → Complete admin takeover
Bonus bounties: Reset token leak, authentication bypass
```

### 3. Demonstrate Business Impact

```
Don't just say: "IDOR in user API"

Instead demonstrate:
→ Accessed 10,000 user records
→ Extracted customer PII (names, emails, phone)
→ Exported customer data to CSV
→ Identified admin users
→ Total: $500,000 in customer data exposed

This proves impact = higher bounty
```

### 4. Document Everything

```
Screenshot evidence:
✓ Before/after showing different user data
✓ Request/response showing IDOR
✓ Tools used (Burp, curl, custom script)
✓ Timeline of discovery
✓ Proof of data extraction
```

---

## Claude's Hunting Recommendations

When you run a hunt, Claude provides:

### For Each Target Vulnerability:

1. **Why It's Likely**
   - Based on technology stack
   - Common patterns in this setup
   - Bug bounty data shows prevalence

2. **Discovery Method**
   - Exact steps to find it
   - Tools to use
   - Parameters to test
   - Indicators to look for

3. **Exploitation**
   - Step-by-step walkthrough
   - Payloads to use
   - Expected responses
   - How to verify success

4. **Impact**
   - What data is exposed
   - Business consequences
   - Severity level
   - Estimated bounty

5. **Next Steps**
   - How to chain it
   - Privilege escalation paths
   - Related vulnerabilities
   - If found, what to do next

---

## Results & Reporting

### Hunting Report Includes

```json
{
  "assessment_id": "bug-hunt-20260921-143022",
  "target": "https://app.example.com",
  "summary": {
    "total_hunted": 15,
    "confirmed_findings": 6,
    "potential_bounty": 15500,
    "hunting_efficiency": 40%
  },
  "findings": [
    {
      "vulnerability": "IDOR in /api/users/{id}",
      "type": "Insecure Direct Object References",
      "severity": "High",
      "bounty_estimate": 2000,
      "steps": [...],
      "proof_of_concept": "..."
    },
    ...
  ],
  "recommendations": [...],
  "next_steps": [...]
}
```

### Metrics Tracked

- **Hunting Efficiency**: Findings / Targets tested
- **Average Bounty**: Total / Number of findings
- **ROI**: Bounty value / Time spent
- **Quick Wins**: Easy-to-find, high-value findings
- **Chaining Opportunities**: Related vulnerabilities

---

## Best Practices

### 1. Start with Quick Wins

```
Test in order:
1. Check IDOR in every ID parameter
2. Test client-side authorization
3. Check for exposed secrets in JS
4. Look for S3/storage misconfigurations
5. Then move to complex vulnerabilities
```

### 2. Follow Claude's Guidance

Claude recommends hunting targets based on:
- Technology stack match
- Bug bounty data
- Expected bounty value
- Discovery difficulty

Trust the ranking by ROI.

### 3. Document As You Go

```
Save:
✓ Screenshots of findings
✓ Request/response pairs
✓ Console output
✓ Proof of impact
✓ Timeline of activities
```

### 4. Verify Everything

```
Before claiming vulnerability:
✓ Can you reproduce it consistently?
✓ Is it a real security issue?
✓ Have you tested edge cases?
✓ Could it be a test/staging endpoint?
✓ Is it actually exploitable?
```

### 5. Demonstrate Impact

```
Not just: "Parameter reflects input"
But: "User input reflects in error message, allowing XSS 
     to steal admin session cookies"

This justifies higher bounty value.
```

---

## Security Considerations

### Authorization

⚠️ **ONLY hunt on systems you have written permission to test.**

Unauthorized access is illegal. Ensure you have:
- Written penetration testing agreement
- Clear scope definition
- Client authorization
- Insurance coverage

### Data Handling

✓ Don't extract more data than necessary  
✓ Don't modify or delete data  
✓ Don't access other users' sensitive data  
✓ Report findings responsibly  
✓ Delete any data you downloaded  

### Responsible Disclosure

1. Find vulnerability
2. Document thoroughly
3. Report to client/program
4. Give reasonable time to patch (typically 90 days)
5. Only publish after fix is available

---

## Integration with Main Assessment

Use bug bounty hunting as part of complete assessment:

```bash
# 1. Run AI assessment
vapt ai interactive --client "Acme" --target "https://app.acme.com"

# 2. Run bug bounty hunt based on findings
vapt bug-bounty hunt --client "Acme" --target "https://app.acme.com"

# 3. Combine results into final report
# Both AI assessment and bug hunt findings compiled
```

---

## Summary

The bug bounty hunting engine provides:

✓ **YesWeHack data integration** - Learn from real reports  
✓ **Claude-powered analysis** - Intelligent vulnerability prioritization  
✓ **ROI-focused hunting** - $1000-$5000+ bounties  
✓ **Systematic methodology** - Repeatable process  
✓ **Professional reporting** - Hunt result documentation  

Perfect for:
- Bug bounty hunters
- Penetration testers
- Security researchers
- Organizations improving security posture

---

**Start hunting:** `vapt bug-bounty hunt --target "https://your-target.com"`

Claude will guide you to high-value vulnerabilities! 💰🔐
