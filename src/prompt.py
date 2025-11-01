from datetime import datetime
from typing import Dict, Any

# Utility function to safely format prompts with content that may contain curly braces
def safe_format(template: str, **kwargs: Any) -> str:
    """
    Safely format a template string, escaping any curly braces in the values.
    This prevents ValueError when content contains unexpected curly braces.
    """
    # Escape any curly braces in the values
    safe_kwargs = {k: v.replace('{', '{{').replace('}', '}}') if isinstance(v, str) else v
                  for k, v in kwargs.items()}
    return template.format(**safe_kwargs)

# Get current date in a readable format
def get_current_date():
    return datetime.now().strftime("%B %d, %Y")

#=====================================

query_writer_instructions_legal = """
You are an expert research assistant generating search queries for legal and financial issues related to: {topic}

**CURRENT DATE: {current_date}. Prioritize recent developments from 2024-2025.**

Generate {number_queries} targeted search queries covering:

- Regulatory actions (SEBI, MCA, NCLT, SAT)
- Litigation and legal disputes  
- Financial irregularities and audit issues
- Corporate governance concerns
- Director-related issues and compliance

Use domain-specific terms and site filters where helpful.

Return JSON format:
{{"query": ["query1", "query2", ...]}}

Research Topic: {topic}

Example:
Research Topic: Are there any legal or financial issues affecting Tata Motors Ltd.?

Output:
```json
{{
  "query": [
    "Tata Motors Ltd. legal cases site:https://indiankanoon.org/",
    "Tata Motors Ltd. legal cases site:https://www.casemine.com",
    "Tata Motors Ltd. legal cases site:https://airrlaw.com/",
    "Tata Motors Ltd. NCLT cases site:https://nclt.gov.in/",
    "Tata Motors Ltd. SAT appeals site:https://sat.gov.in/",
    "Tata Motors Ltd. SEBI regulatory actions site:https://sebi.gov.in/",
    "Tata Motors Ltd. audit qualifications site:nseindia.com OR site:bseindia.com",
    "Tata Motors Ltd. corporate governance issues site:bseindia.com",
    "Tata Motors Ltd. MCA filings site:mca.gov.in",
    "Tata Motors Ltd. ratings news",
    "Tata Motors Ltd. Director resignations news",
    "Tata Motors Ltd. Director cases news",
    "Tata Motors Ltd. Complaints against Directors",
    "Tata Motors Ltd. SAT appeals site:sat.gov.in",
    "Tata Motors Ltd. forensic audit news",
  ]
}}```

Research Topic: {topic}
"""
#======================================
query_writer_instructions_macro = """You are a global macro research assistant analyzing a specific commodity mentioned in the research topic: {topic}. Your goal is to uncover insights into market dynamics, pricing trends, recent events, and fundamental global factors influencing the commodity.

**CURRENT DATE CONTEXT: Today is {current_date}. PRIORITIZE the most recent information available, particularly developments from the start of the current year. Always search for the latest updates and current developments.**

Generate {number_queries} commodity research queries using:
    - Focus each query on a specific dimension of the commodity's macro landscape.
    - Use authoritative filters or context signals (e.g., site:eia.gov, site:bloomberg.com).
    - Employ terms like “price outlook”, “supply risk”, “demand forecast”, “inventory buildup”, “producer sentiment”, “OPEC decision”.
    - Aim for queries that reveal near-term and medium-term implications.

Format:
- Format your response as a JSON object with this key:
   - "query": A list of search queries.

Example:
Research Topic: What are the near-term risks to crude oil prices globally?

Output:
```json
{{
  "query": [
    "Crude oil price outlook July 2025 site:bloomberg.com OR site:reuters.com",
    "Global oil inventory levels site:eia.gov",
    "OPEC supply adjustment July 2025 site:opec.org",
    "Oil demand forecast medium term site:imf.org OR site:worldbank.org",
    "Impact of recent shipping disruptions on crude oil prices site:ft.com",
    "Effect of U.S. interest rates on commodity prices site:bloomberg.com",
    "Strategic petroleum reserve releases impact site:eia.gov",
    "Brent vs WTI price divergence July 2025 site:oilprice.com"
  ]
}}```

Research Topic: {topic}
"""

#======================================

query_writer_instructions_general = """You are a research assistant exploring: {topic}

**CURRENT DATE: {current_date}. Prioritize developments from the start of the current year.**

Generate {number_queries} search queries covering key aspects:
- Historical context and background
- Recent developments and news
- Expert perspectives and analysis
- Controversies and debates
- Policy and regulatory aspects

Use site-specific constraints where helpful (e.g., site:nature.com, site:nytimes.com).
    - One aspect per query (no multitopic prompts).
    - Avoid redundancy, but allow flexibility in phrasing to account for diverse search engine results.
    - You may include site-specific constraints where helpful (e.g., site:nature.com, site:nytimes.com).
    - Prefer phrasing that mirrors how users naturally ask questions.

Format:
- Format your response as a JSON object with this key:
   - "query": A list of search queries.

Example:
Research Topic: What are the scientific and policy issues around climate geoengineering?

Output:
```json
{{
  "query": [
    "History of geoengineering techniques site:wikipedia.org",
    "Solar radiation management risks site:nature.com",
    "Geoengineering policy positions US EU China site:ipcc.ch",
    "Recent controversies in climate geoengineering site:nytimes.com",
    "Long-term effectiveness of climate engineering site:sciencedirect.com",
    "Climate scientist perspectives on geoengineering site:noaa.gov"
  ]
}}```

Research Topic: {topic}
"""

#======================================
web_search_validation_instructions = """Evaluate search results in relation to a query".

Instructions:
- You are provided with a search result consisting of a link and a snippet of information that is present at the link address.
- Look at the snippet and keeping in mind the {query} and the {current_date}, answer whether the search result is relevant or not.
- If relevant, answer with a simple message "yes", else "no'.
- Do not add any further text to your response.

QUERY:
{query}
"""

#=======================================
reflection_instructions = """You are an expert research assistant analyzing answers about "{research_topic}".

Instructions:
- Identify knowledge gaps or areas that need deeper exploration and generate a follow-up query. (1 or multiple).
- If provided answers are sufficient to answer the user's question, don't generate a follow-up query.
- If there is a knowledge gap, generate a follow-up query that would help expand your understanding.
- Focus on technical details, implementation specifics, or emerging trends that weren't fully covered.

Requirements:
- Ensure the follow-up query is self-contained and includes necessary context for web search.

Output Format:
- Format your response as a JSON object with these exact keys:
   - "is_sufficient": true or false
   - "knowledge_gap": Describe what information is missing or needs clarification
   - "follow_up_queries": Write a specific question to address this gap

Example:
```json
{{
    "is_sufficient": true, // or false
    "knowledge_gap": "The summary lacks information about performance metrics and benchmarks", // "" if is_sufficient is true
    "follow_up_queries": ["What are typical performance benchmarks and metrics used to evaluate [specific technology]?"] // [] if is_sufficient is true
}}
```

Reflect carefully on the Summaries to identify knowledge gaps and produce a follow-up query. Then, produce your output following this JSON format:

Answers:
{summaries}
"""

#================================================
reflection_instructions_modified = """You are an expert research assistant analyzing extracted information about "{research_topic}".

    Instructions:
    - Evaluate the provided extracted information to determine if it is sufficient to answer the original user question.
    - If the extracted information is sufficient, set "is_sufficient" to true and leave "knowledge_gap" and "follow_up_queries" as empty/null.
    - If the extracted information is NOT sufficient, identify knowledge gaps or areas that need deeper exploration based on the original user question and the provided extracted information.
    - For each identified knowledge gap, generate 1 or multiple specific follow-up queries that would help expand your understanding to fully answer the original user question.
    - Focus on technical details, implementation specifics, or emerging trends that weren't fully covered in the extracted information.

    Requirements:
    - Ensure any follow-up query is self-contained and includes necessary context for web search.

    Output Format:
    - Format your response as a JSON object with these exact keys:
       - "is_sufficient": true or false
       - "knowledge_gap": Describe what information is missing or needs clarification (empty string if is_sufficient is true)
       - "follow_up_queries": Write a list of specific questions to address this gap (empty array if is_sufficient is true)

    Example:
    ```json
    {{
        "is_sufficient": true, // or false
        "knowledge_gap": "The summary lacks information about performance metrics and benchmarks", // "" if is_sufficient is true
        "follow_up_queries": ["What are typical performance benchmarks and metrics used to evaluate [specific technology]?"]
    }}
    ```

    Reflect carefully on the Extracted Information to identify knowledge gaps and produce a follow-up query if necessary. Then, produce your output following this JSON format:

    Extracted Information:
    {extracted_info_json}
    """
#=================================================

report_writer_instructions_legal = """
# Legal & Financial Risk Report: {research_topic}

## Date: {current_date}

Write a comprehensive report analyzing legal and financial developments affecting the company. Focus on actionable insights for decision-makers.

**Structure:**
- **Company Profile**: Business model, sector, recent performance
- **Legal Landscape**: Regulatory actions, litigation, governance issues
- **Financial Impact**: Revenue effects, compliance costs, investor perception
- **Strategic Response**: Company actions and mitigation strategies  
- **Risk Outlook**: Short-term (0-6 months) and medium-term (6-18 months) threats
- **Benchmarks**: Peer comparisons and industry trends

**Requirements:**
- Use markdown formatting with clear headings and structure
- Cite all claims from summaries using [1], [2] notation
- Include reference list at end
- Start directly with content, no introductory sections
- Use full token capacity for thorough analysis

**Data Source:** {summaries}
"""

#======================================

query_writer_instructions_deepsearch = """
You are a deep search assistant tasked with uncovering the most recent, relevant and information about the topic: {topic}. Your goal is to produce high-coverage search queries that maximize factual discovery across trusted sources.

**CURRENT DATE CONTEXT: Today is {current_date}. PRIORITIZE the most recent information available, particularly developments from 2024-2025. Always search for the latest updates and current developments.**

---

## OBJECTIVE

- Focus on **information retrieval**, not interpretation.
- Prioritize **recency**, **coverage**, and **source diversity**.
- Avoid speculative or opinion-based phrasing.

---

## INSTRUCTIONS

1. Break down the topic into granular subtopics (e.g., recent developments, key players, controversies, data points).
2. Generate queries that target **latest news**, **official updates**, **expert commentary**, and **primary sources**.
3. Use filters like `site:reuters.com`, `site:gov.in`, `site:bloomberg.com`, `site:business-standard.com`, etc.
4. Include date signals (e.g., “August 2025”, “last 6 months”) where helpful.
5. Avoid multitopic prompts — each query should target one aspect.
6. Ensure queries are phrased naturally for search engines.

---

## FORMAT

Return a JSON object with:
- "query": A list of search queries.

Example:
Research Topic: Recent developments in Adani Group’s financial disclosures

Output:
```json
{{
  "query": [
    "Adani Group financial disclosures August 2025 site:business-standard.com",
    "Adani Group audit notes site:nseindia.com OR site:bseindia.com",
    "Adani Group credit rating changes 2025 site:crisil.com",
    "Adani Group debt restructuring news site:reuters.com",
    "Adani Group SEBI updates site:sebi.gov.in",
    "Adani Group financial filings site:mca.gov.in"
  ]
}}```

Research Topic: {topic}
"""


#======================================

query_writer_instructions_person_search = """
You are a research assistant generating ethical search queries for person research: {topic}

**CURRENT DATE: {current_date}. Prioritize recent developments.**

Generate {number_queries} platform-specific search queries covering:
- Professional background (LinkedIn, Naukri.com)
- Social media presence (Twitter, Facebook, Instagram)  
- Legal/business records (IndiaKanoon.org, CaseMine.com)
- Educational background and achievements
- Public statements and professional activities

Focus only on publicly available information and ethical research practices.

---

## TASK INSTRUCTIONS

Generate at least **{number_queries}** targeted search queries:
- Platform-specific queries using site: filters
- Professional background and career queries
- Social media presence queries
- Legal and regulatory involvement queries
- Educational and achievement-based queries
- Cross-platform verification queries

---

## Response Format

Return your output as a **JSON object** with this key:
   - "query": A list of search queries targeting different platforms and information types.

Example:
Research Topic: Create a profile of Sundar Pichai

Output:
```json
{{
  "query": [
    "Sundar Pichai LinkedIn profile site:linkedin.com",
    "Sundar Pichai career background site:naukri.com",
    "Sundar Pichai Google CEO site:facebook.com",
    "Sundar Pichai tweets technology leadership site:twitter.com",
    "Sundar Pichai Instagram professional site:instagram.com",
    "Sundar Pichai legal cases site:indiankanoon.org",
    "Sundar Pichai court cases site:casemine.com",
    "Sundar Pichai regulatory matters site:airrlaw.com",
    "Sundar Pichai IIT Stanford education background",
    "Sundar Pichai awards achievements recognition",
    "Sundar Pichai interviews statements public speaking",
    "Sundar Pichai business ventures investments"
  ]
}}```

Research Topic: {topic}
"""
#======================================

report_writer_instructions_general = """
# Research Report: {research_topic}

## Date
{current_date}

## Objective
Produce a detailed and structured report addressing the user's research topic. The report must be fact-rich, well-organized, and suitable for informed decision-makers, stakeholders, or analysts across industries.

---

## Contextual Overview
- Begin with an in-depth analysis of the current all relevant aspects relevant to {research_topic}, and list precise facts if available.
- Highlight recent developments, key players, policy updates, technological shifts, or public sentiment where applicable.
- Include supportive examples and cite factual content from the provided data summaries.

---

## Thematic Analysis
- Identify 3-5 major themes or areas of discussion emerging from the research topic.
- For each theme, include:
  - Historical context or origin
  - Current implications
  - Future possibilities or concerns
  - Supporting evidence and citations from provided content

---

## Data Insights
- Use any quantifiable information (statistics, trends, financials, projections) extracted from summaries.
- Present using bullet points, tables, or code blocks for clarity.
- Visual structure should enhance readability and insight.

---

## Risks & Uncertainties
- Analyze unknowns, open questions, and potential risk factors.
- Discuss what is missing from public discourse, data gaps, or controversial viewpoints.
- Use markdown callouts (e.g., blockquotes or bolded statements) to make this section stand out.

---

## Citations & References
- All claims derived from summaries must be cited using [1], [2], etc.
- Provide a reference list at the end, matching the bracketed numbers throughout the text.

---

## Writing Guidelines
- Begin directly with the # Title. Avoid generic preambles like “Introduction” or “Executive Summary.”
- Use markdown features: headings (`#`, `##`, `###`), bold, italics, horizontal rules
"""

#======================================

query_writer_instructions_investment = """
You are an investment research assistant generating search queries for: {topic}

**CURRENT DATE: {current_date}. Prioritize 2024-2025 developments.**

Generate {number_queries} investment research queries covering:
- Financial performance and metrics
- Business fundamentals and competitive position
- Growth prospects and market opportunities
- Valuation metrics and peer comparisons
- Risk factors and regulatory compliance
- Management quality and strategic direction

Target financial databases, exchanges, analyst reports, and credible business sources.

---

## TASK INSTRUCTIONS

Generate at least **{number_queries}** targeted investment research queries:
- Financial performance and metrics queries
- Business fundamentals and competitive position queries
- Management and governance analysis queries
- Market opportunity and growth prospect queries
- Risk assessment and regulatory compliance queries
- Peer comparison and sector analysis queries

---

## Response Format

Return your output as a **JSON object** with this key:
   - "query": A list of search queries targeting different aspects of investment analysis.

Example:
Research Topic: Investment analysis of Reliance Industries Ltd

Output:
```json
{{
  "query": [
    "Reliance Industries quarterly results Q2 2025",
    "Reliance Industries annual report 2024-25 financial performance site:ril.com",
    "Reliance Industries debt equity ratio cash flow analysis site:screener.in",
    "Reliance Industries Jio ARPU subscriber growth metrics site:moneycontrol.com",
    "Reliance Industries retail expansion strategy growth plans site:economictimes.indiatimes.com",
    "Reliance Industries green energy investment capex plans site:livemint.com",
    "Reliance Industries valuation PE ratio analyst target price site:investing.com",
    "Reliance Industries vs Asian Paints vs HDFC Bank peer comparison site:valueresearchonline.com",
    "Reliance Industries management commentary investor call transcript",
    "Reliance Industries ESG rating sustainability initiatives site:sustainalytics.com",
    "Reliance Industries regulatory compliance SEBI filings site:sebi.gov.in",
    "Reliance Industries oil refining margins GRM analysis site:bloomberg.com"
  ]
}}```

Research Topic: {topic}
"""

#======================================
report_writer_instructions_macro = """
# Commodity Macro Report: {research_topic}

## Date
{current_date}

## Purpose
Produce a comprehensive macroeconomic report focused on the commodity mentioned in the user's research topic. This report is intended for professional economic analysts and investment decision-makers.

---

## Recent Developments
- Begin with an in-depth overview of recent price trends, geopolitical shifts, regulatory updates, and macroeconomic conditions impacting {research_topic}.
- Include relevant global events, policy announcements, and institutional positions.
- Use paragraph form with examples and cite supporting data from the summaries.

---

## Market Dynamics
### Supply & Demand Analysis
- Examine seasonal effects, trade flows, inventories, and producer/consumer behavior.
- Explore macroeconomic influences such as interest rates, inflation, and currency volatility.
- Use tables and cited data for clarity.

### Outlook
- Short-Term (0=3 months): Provide concrete forecasts and expectations.
- Medium-Term (3=12 months): Highlight structural trends, risks, and emerging signals.

---

## Risks & Uncertainties
- Analyze potential disruptions including policy shifts, weather anomalies, supply chain instability, and political tensions.
- Use bullet points or markdown formatting to make risks stand out.

---

## Theoretical Context & Applications
- Discuss historical trends, economic models relevant to commodity pricing, and global macroeconomic theories.
- Incorporate regional case studies and comparative analysis when possible.

---

## References
- All factual claims derived from summaries must be cited using [1], [2], etc.
- Provide a final reference list at the end using bracketed numeric citations.

---

## Writing & Formatting Requirements
- **Start directly with the # Title. Avoid preambles like 'Research Framework' or 'Objective'.**
- Use markdown (`#`, `##`, `**bold**`, `_italic_`, tables, horizontal rules) for structured readability.
- Ensure sufficient spacing and paragraph depth throughout.
- Use the full available token budget. Prioritize insight density over brevity.
- Maintain a confident yet analytical tone.

---

## User Context
**Research Topic:** {research_topic}

## Summarized Inputs
{summaries}
"""
#================================================================================

report_writer_instructions_deepsearch = """
# Factual Summary Report: {research_topic}

## Date
{current_date}

## Objective
Present a highly detailed report providing in-depth coverage of ALL relevant information about the research topic, with priority accorded to more recent information. This report is intended for users who want direct access to verified updates without interpretation or analysis.

---

## Key Findings
- List the ALL facts, events, or updates discovered during the search.
- Use bullet points or short paragraphs.
- Include dates, names, and source references where available.
- Avoid speculation or commentary.

---

## Source Highlights
- Mention the leading (top-10) informative sources (e.g., Bloomberg, Reuters, SEBI, MCA, etc.).
- Note any discrepancies or gaps in coverage.
- If multiple sources confirm the same fact, mention that.

---

## References
- Use bracketed numeric citations [1], [2], etc. for any factual claims.
- Provide a reference list at the end with source URLs or publication names.

---

## Formatting Guidelines
- Use markdown formatting: headings (`#`, `##`), bullet points, bold, horizontal rules.
- Keep tone neutral and factual.
- Avoid interpretation, synthesis, or opinion.

---

## 🔎 User Context
**Research Topic:** {research_topic}

## 🧵 Extracted Inputs
{summaries}
"""

#======================================

report_writer_instructions_person_search = """
# Digital Profile Report: {research_topic}

## Date
{current_date}

## Objective
Construct a comprehensive digital profile of the individual based on publicly available information gathered from multiple online platforms, professional networks, social media, and legal databases. This report synthesizes information to create a holistic view of the person's professional background, public presence, and achievements.

---

## Personal & Professional Overview
- Full name, current position, and primary professional affiliations
- Educational background and qualifications
- Career timeline and major professional milestones
- Current role and responsibilities

---

## Professional Network Analysis
### LinkedIn & Professional Presence
- Professional experience and career progression
- Skills, endorsements, and recommendations
- Professional connections and network analysis
- Publications, articles, and thought leadership content

### Career History (Naukri.com & other platforms)
- Employment history and career transitions
- Industry expertise and specializations
- Professional achievements and recognition

---

## Social Media Footprint
### Twitter/X Presence
- Professional opinions and thought leadership
- Industry engagement and discussions
- Public statements and viewpoints
- Follower analysis and influence metrics

### Facebook & Instagram
- Public posts and professional content
- Community involvement and social causes
- Professional brand and public image
- Notable achievements and recognition

---

## Legal & Regulatory Involvement
### Court Cases & Legal Matters
- Any involvement in legal cases (IndiaKanoon.org, CaseMine.com)
- Business litigation or regulatory matters
- Professional legal opinions or expert testimony
- Aviation law involvement (AirLaw.com) if applicable

---

## Achievements & Recognition
- Professional awards and honors
- Industry recognition and accolades
- Speaking engagements and conferences
- Media mentions and interviews
- Published works and research

---

## Digital Reputation Analysis
- Overall online presence and digital footprint
- Professional brand consistency across platforms
- Public perception and sentiment analysis
- Potential reputation risks or concerns

---

## Cross-Platform Verification
- Information consistency across multiple sources
- Verification of claims and achievements
- Identification of any discrepancies or inconsistencies
- Reliability assessment of different information sources

---

## Network & Influence Analysis
- Professional network size and quality
- Industry connections and relationships
- Thought leadership and influence metrics
- Community involvement and social impact

---

## Citations & References
- All information must be cited using bracketed numeric notation [1], [2], etc.
- Include platform sources (LinkedIn, Twitter, Facebook, etc.)
- Provide reference list with source URLs and publication dates

---

## Ethical Considerations & Limitations
- Note any information gaps or unavailable data
- Highlight the distinction between public and private information
- Acknowledge potential privacy boundaries respected
- Mention any information that couldn't be independently verified

---

## Formatting Guidelines
- Use markdown formatting: headings (`#`, `##`), **bold**, _italic_, bullet points, tables
- Maintain professional and respectful tone throughout
- Present information objectively without judgment
- Ensure all claims are properly sourced and verifiable

---

## User Context
**Person Profile Subject:** {research_topic}

## Extracted Information
{summaries}
"""

#======================================

report_writer_instructions_investment = """
# Investment Research Report: {research_topic}

## Date
{current_date}

## Investment Thesis Overview
Provide a comprehensive investment analysis of the company, synthesizing financial performance, business fundamentals, growth prospects, and risk assessment to determine investment attractiveness and provide actionable recommendations.

---

## Executive Summary
- **Investment Recommendation**: Buy/Hold/Sell with rationale
- **Target Price**: Based on valuation analysis (if applicable)
- **Key Investment Highlights**: Top 3-5 compelling reasons to invest or avoid
- **Risk Rating**: High/Medium/Low with primary risk factors
- **Investment Horizon**: Short-term vs long-term perspective

---

## Financial Performance Analysis
### Revenue & Profitability
- Revenue growth trends (YoY, QoQ) across business segments
- Margin analysis (Gross, EBITDA, Net) and trend comparison
- Profitability drivers and sustainability assessment

### Balance Sheet Strength
- Debt-to-equity ratios and leverage analysis
- Cash flow generation and working capital management
- Asset quality and return metrics (ROE, ROA, ROIC)

### Key Financial Ratios
- Valuation multiples (P/E, P/B, EV/EBITDA, PEG)
- Efficiency ratios and trend analysis
- Peer comparison and relative valuation

---

## Business Fundamentals Assessment
### Business Model Analysis
- Revenue streams and business segment performance
- Competitive advantages and economic moats
- Market position and industry leadership

### Management Quality
- Track record of management team
- Corporate governance practices
- Strategic vision and execution capabilities
- Capital allocation decisions

### Competitive Landscape
- Market share analysis and positioning
- Key competitors and competitive threats
- Differentiation factors and barriers to entry

---

## Growth Prospects & Opportunities
### Growth Drivers
- Organic growth opportunities and market expansion
- New product launches and innovation pipeline
- Digital transformation and technology adoption
- Acquisition strategy and inorganic growth

### Market Opportunities
- Total addressable market (TAM) analysis
- Emerging market trends and positioning
- Regulatory tailwinds and policy support
- Export potential and international expansion

---

## Risk Analysis
### Business Risks
- Industry cyclicality and market volatility
- Competitive pressures and disruption threats
- Regulatory and compliance risks
- Operational and execution risks

### Financial Risks
- Debt burden and refinancing risks
- Currency exposure and hedging
- Interest rate sensitivity
- Liquidity and cash flow risks

### ESG Considerations
- Environmental impact and sustainability
- Social responsibility and labor practices
- Governance quality and transparency
- ESG-related investment risks and opportunities

---

## Valuation & Price Target
### Valuation Methodology
- Multiple valuation approaches (DCF, comparable multiples, asset-based)
- Key assumptions and sensitivity analysis
- Fair value estimation and price target derivation

### Peer Comparison
- Relative valuation vs industry peers
- Premium/discount analysis and justification
- Sector-specific valuation metrics

---

## Investment Recommendation
### Bull Case Scenario
- Best-case growth assumptions and catalysts
- Upside potential and price targets
- Key positive developments to monitor

### Bear Case Scenario
- Downside risks and negative catalysts
- Worst-case scenario impact assessment
- Early warning indicators to watch

### Base Case Investment Thesis
- Most likely scenario and balanced view
- Risk-adjusted return expectations
- Timeline for investment thesis to play out

---

## Data Sources & References
- All financial data must be cited using bracketed numeric notation [1], [2], etc.
- Include exchange filings, annual reports, analyst reports
- Reference regulatory submissions and management commentary
- Provide source URLs and publication dates

---

## Investment Disclaimers
- Note data limitations and information gaps
- Highlight assumptions and potential changes
- Acknowledge market volatility and risk factors
- Mention that this is research analysis, not investment advice

---

## Formatting Guidelines
- Use markdown formatting: headings (`#`, `##`), **bold**, _italic_, tables, bullet points
- Include financial tables and charts where applicable
- Maintain objective, analytical tone throughout
- Support all claims with proper citations and data

---

## Investment Context
**Company Analysis Subject:** {research_topic}

## Financial & Business Data
{summaries}
"""

#================================================================================
