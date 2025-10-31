# question_analyzer.py
# Utility functions to analyze user questions and extract specific information requirements

import re
from typing import Dict, List, Optional, Tuple

def analyze_research_question(question: str) -> Dict[str, any]:
    """
    Analyze a research question to identify what specific information is being requested.
    
    Args:
        question: The user's research question
        
    Returns:
        Dictionary containing analysis of the question requirements
    """
    question_lower = question.lower()
    
    # Identify question type
    question_type = identify_question_type(question)
    
    # Look for specific information requests
    specific_requests = extract_specific_requests(question)
    
    # Identify entities and topics
    entities = extract_entities(question)
    
    # Determine urgency and specificity level
    specificity_level = assess_specificity_level(question)
    
    # Look for temporal requirements
    temporal_context = extract_temporal_context(question)
    
    return {
        "question_type": question_type,
        "specific_requests": specific_requests,
        "entities": entities,
        "specificity_level": specificity_level,
        "temporal_context": temporal_context,
        "keywords": extract_keywords(question),
        "requires_numeric_data": requires_numeric_data(question),
        "requires_comparison": requires_comparison(question),
        "requires_list": requires_list(question)
    }


def identify_question_type(question: str) -> str:
    """Identify the type of question being asked."""
    question_lower = question.lower()
    
    # Factual/data questions
    if any(word in question_lower for word in ['what is', 'what are', 'how much', 'how many', 'when did', 'where is']):
        return "factual"
    
    # Analytical questions
    elif any(word in question_lower for word in ['why', 'how does', 'what causes', 'what impact', 'analyze']):
        return "analytical"
    
    # Comparison questions
    elif any(word in question_lower for word in ['compare', 'versus', 'vs', 'difference between', 'better than']):
        return "comparison"
    
    # Trend/temporal questions
    elif any(word in question_lower for word in ['trend', 'over time', 'since', 'growth', 'change', 'evolution']):
        return "trend"
    
    # List/enumeration questions
    elif any(word in question_lower for word in ['list', 'examples of', 'types of', 'kinds of', 'which']):
        return "enumeration"
    
    # Evaluation questions
    elif any(word in question_lower for word in ['evaluate', 'assess', 'review', 'opinion', 'should']):
        return "evaluation"
    
    return "general"


def extract_specific_requests(question: str) -> List[str]:
    """Extract specific information requests from the question."""
    question_lower = question.lower()
    requests = []
    
    # Numeric/quantitative requests
    numeric_patterns = [
        r'value of (\w+)',
        r'price of (\w+)',
        r'cost of (\w+)',
        r'revenue of (\w+)',
        r'market cap of (\w+)',
        r'percentage of (\w+)',
        r'number of (\w+)',
        r'amount of (\w+)',
        r'size of (\w+)'
    ]
    
    for pattern in numeric_patterns:
        matches = re.findall(pattern, question_lower)
        for match in matches:
            requests.append(f"numeric_value: {match}")
    
    # Specific entity requests
    entity_patterns = [
        r'ceo of (\w+)',
        r'founder of (\w+)', 
        r'headquarters of (\w+)',
        r'subsidiary of (\w+)',
        r'competitor of (\w+)'
    ]
    
    for pattern in entity_patterns:
        matches = re.findall(pattern, question_lower)
        for match in matches:
            requests.append(f"entity_info: {match}")
    
    # Date/time requests
    if any(word in question_lower for word in ['when', 'date', 'year', 'month']):
        requests.append("temporal_info")
    
    # List requests
    if any(word in question_lower for word in ['list', 'examples', 'types']):
        requests.append("list_items")
    
    return requests


def extract_entities(question: str) -> List[str]:
    """Extract named entities and important nouns from the question."""
    # Simple entity extraction - could be enhanced with NLP libraries
    
    # Common entity patterns
    entity_patterns = [
        r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Company names, person names
        r'\b[A-Z]{2,}\b',  # Acronyms
        r'\$\d+',  # Dollar amounts
        r'\d+%',   # Percentages
        r'\d{4}',  # Years
    ]
    
    entities = []
    for pattern in entity_patterns:
        matches = re.findall(pattern, question)
        entities.extend(matches)
    
    # Extract quoted entities
    quoted = re.findall(r'"([^"]*)"', question)
    entities.extend(quoted)
    
    return list(set(entities))  # Remove duplicates


def assess_specificity_level(question: str) -> str:
    """Assess how specific vs general the question is."""
    question_lower = question.lower()
    
    specific_indicators = [
        'exact', 'precise', 'specific', 'detailed', 'comprehensive',
        'value', 'amount', 'number', 'percentage', 'date', 'year'
    ]
    
    general_indicators = [
        'overview', 'general', 'summary', 'about', 'regarding', 'concerning'
    ]
    
    specific_count = sum(1 for indicator in specific_indicators if indicator in question_lower)
    general_count = sum(1 for indicator in general_indicators if indicator in question_lower)
    
    if specific_count > general_count:
        return "high"
    elif general_count > specific_count:
        return "low"
    else:
        return "medium"


def extract_temporal_context(question: str) -> Optional[str]:
    """Extract temporal context from the question."""
    question_lower = question.lower()
    
    temporal_patterns = [
        r'in (\d{4})',           # "in 2023"
        r'since (\d{4})',        # "since 2020"
        r'from (\d{4}) to (\d{4})',  # "from 2020 to 2023"
        r'over the (last|past) (\w+)',  # "over the last year"
        r'(current|latest|recent)',     # Current/latest/recent
        r'(quarterly|annually|monthly)', # Time periods
    ]
    
    for pattern in temporal_patterns:
        match = re.search(pattern, question_lower)
        if match:
            return match.group(0)
    
    return None


def extract_keywords(question: str) -> List[str]:
    """Extract important keywords from the question."""
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'among', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
        'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'
    }
    
    # Extract words, remove punctuation and convert to lowercase
    words = re.findall(r'\b[a-zA-Z]+\b', question.lower())
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    return keywords


def requires_numeric_data(question: str) -> bool:
    """Check if the question requires numeric data."""
    question_lower = question.lower()
    numeric_indicators = [
        'value', 'price', 'cost', 'amount', 'number', 'count', 'total',
        'revenue', 'profit', 'income', 'expense', 'budget', 'market cap',
        'percentage', 'percent', '%', 'rate', 'ratio', 'metric', 'figure',
        'how much', 'how many', 'quantify', 'measure'
    ]
    
    return any(indicator in question_lower for indicator in numeric_indicators)


def requires_comparison(question: str) -> bool:
    """Check if the question requires comparison."""
    question_lower = question.lower()
    comparison_indicators = [
        'compare', 'versus', 'vs', 'against', 'difference', 'similar',
        'better', 'worse', 'higher', 'lower', 'more', 'less', 'than',
        'contrast', 'relative to', 'compared to'
    ]
    
    return any(indicator in question_lower for indicator in comparison_indicators)


def requires_list(question: str) -> bool:
    """Check if the question requires a list or enumeration."""
    question_lower = question.lower()
    list_indicators = [
        'list', 'examples', 'types', 'kinds', 'categories', 'which',
        'what are', 'include', 'such as', 'enumerate', 'name'
    ]
    
    return any(indicator in question_lower for indicator in list_indicators)


def generate_extraction_instructions(analysis: Dict[str, any]) -> str:
    """Generate specific extraction instructions based on question analysis."""
    instructions = []
    
    # Base instruction
    instructions.append("EXTRACT SPECIFIC INFORMATION to answer the user's question directly.")
    
    # Add specific instructions based on analysis
    if analysis["requires_numeric_data"]:
        instructions.append("FIND and PRESENT exact numbers, values, percentages, and quantitative data.")
    
    if analysis["requires_comparison"]:
        instructions.append("LOCATE comparison data and present it clearly with specific metrics.")
    
    if analysis["requires_list"]:
        instructions.append("COMPILE a comprehensive list of items that answer the question.")
    
    if analysis["temporal_context"]:
        instructions.append(f"FOCUS on information relevant to the time period: {analysis['temporal_context']}")
    
    if analysis["specificity_level"] == "high":
        instructions.append("PRIORITIZE specific, detailed, and precise information over general analysis.")
    
    if analysis["entities"]:
        entities_str = ", ".join(analysis["entities"][:3])  # Show first 3 entities
        instructions.append(f"PAY SPECIAL ATTENTION to information about: {entities_str}")
    
    return " ".join(instructions)


# Example usage
if __name__ == "__main__":
    # Test the analyzer
    questions = [
        "What is the market cap of Apple in 2024?",
        "Compare the revenue of Microsoft and Google",
        "List the top 5 competitors of Tesla",
        "Analyze the impact of AI on healthcare",
        "What are the quarterly earnings of Amazon since 2022?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        analysis = analyze_research_question(question)
        print(f"Analysis: {analysis}")
        print(f"Instructions: {generate_extraction_instructions(analysis)}")