# Questions to Ask About Statement of Comprehensive Income

Run this command to start interactive Q&A:
```bash
python3 analyze_annual_report.py samples/q3-2026-inf.pdf --interactive
```

Then ask these questions to understand the income statement in detail:

## 1. Get the Full Picture

```
Show me the complete Statement of Comprehensive Income with ALL line items for Q3 FY2026 (December 31, 2025) vs Q3 FY2025 (December 31, 2024). Include amounts in ₹ crore and growth rates.
```

## 2. Revenue Analysis

```
What was the revenue in Q3 (Dec 31, 2025) vs Q3 (Dec 31, 2024)? Show me both in ₹ crore and USD millions with growth rates.
```

## 3. Cost of Sales Deep Dive

```
Analyze Cost of Sales: It was ₹32,652 crore in Q3 2025 vs ₹29,120 crore in Q3 2024 (12.1% growth). Why did it grow faster than revenue (8.9%)? What's driving this?
```

## 4. Gross Profit Analysis

```
Calculate the Gross Profit and Gross Margin for both quarters. What changed and why?
```

## 5. Operating Expenses Breakdown

```
Break down Operating Expenses:
- Selling and marketing: ₹2,292 vs ₹1,839 crore (24.6% growth!)
- G&A: ₹2,180 vs ₹1,893 crore (15.2% growth)

Why did these expenses grow so much? What's driving it?
```

## 6. Operating Profit Analysis

```
Operating Profit was ₹8,355 crore (Q3 2025) vs ₹8,912 crore (Q3 2024) - a DECLINE of 6.3% despite revenue growing 8.9%. Walk me through what happened between Revenue and Operating Profit to cause this.
```

## 7. Tax Analysis

```
Income tax expense was ₹2,563 crore vs ₹2,848 crore - actually DECREASED. Calculate the effective tax rate for both quarters. Why did tax go down?
```

## 8. Net Profit Analysis

```
Net profit was ₹6,654 crore vs ₹6,806 crore (down 2.2%). Why did profit decline when revenue grew? What are the top 3 reasons?
```

## 9. Margin Compression

```
Calculate these margins for both Q3 2025 and Q3 2024:
- Gross Margin %
- Operating Margin %
- Net Margin %

Show me the margin compression and explain what's causing it.
```

## 10. Nine-Month Trend

```
Compare the nine months ended December 31, 2025 vs 2024. Is the margin compression trend getting better or worse? Show me the numbers.
```

## 11. USD Impact

```
Revenue growth was 8.9% in INR but only 3.2% in USD. What does this tell us about currency impact? Show me the same analysis for profits in USD terms.
```

## 12. Cost Structure Issue

```
Revenues grew 8.9% but:
- Cost of Sales grew 12.1%
- Selling expenses grew 24.6%
- G&A grew 15.2%

Why are ALL costs growing faster than revenue? Is this sustainable? What needs to change?
```

## 13. EPS Analysis

```
Basic EPS was ₹16.17 vs ₹16.43 (down 1.6%). Net profit declined 2.2%. Why is the EPS decline smaller? What happened to share count?
```

## 14. Operating Leverage

```
This company had negative operating leverage - revenue up 8.9%, operating profit down 6.3%. Calculate the operating leverage and explain what this means for Infosys's business model.
```

## 15. Investment Recommendation

```
Based on this income statement analysis, what's your investment recommendation? Is Infosys a buy, hold, or sell? What are the key risks and opportunities?
```

---

## Pro Tips:

1. **Start broad, then drill down**: Begin with questions 1-2 to get overview, then deep dive into specific areas

2. **Ask follow-ups**: After each answer, ask "Why?" or "Can you elaborate?" to go deeper

3. **Compare periods**: Always ask for both Q3 and 9-month comparisons to see trends

4. **Cross-reference**: Ask Claude to verify numbers against the ratio analysis section

5. **Real business impact**: Ask "What does this mean for..." to get practical insights

---

## Quick Start:

```bash
# Start interactive session
python3 analyze_annual_report.py samples/q3-2026-inf.pdf --interactive

# Then paste your questions one by one
# Or combine multiple questions in one prompt for deeper analysis
```

**Example Combined Question:**
```
I want to understand why Operating Profit declined 6.3% when Revenue grew 8.9%.

Please:
1. Show me the full income statement for Q3 2025 vs Q3 2024
2. Calculate the bridge from Revenue to Operating Profit
3. Identify which cost line items grew the most
4. Explain the root causes
5. Calculate the margin compression at each level

Use actual numbers from the document.
```

This will give you a comprehensive analysis in one go!
