# Report Word Limits Update

## Changes Made

Updated the INTELLISEARCH application to use new word limits for reports as requested:

### Previous Limits:
- **Concise Report**: Maximum 500 words
- **Detailed Report**: Maximum 1500 words

### New Limits:
- **Concise Report**: 600-1200 words (minimum 600, maximum 1200)
- **Detailed Report**: 800-3000 words (minimum 800, maximum 3000)

## Files Modified

### src/nodes.py
Updated the following configurations:

#### 1. Core Word Limits
- **Concise max_words**: 500 → 1200
- **Detailed max_words**: 1500 → 3000
- **Concise default_section_words**: 125 → 300
- **Detailed default_section_words**: 300 → 600

#### 2. Minimum Word Thresholds  
- **Concise minimum**: 200 → 600 words
- **Detailed minimum**: 500 → 800 words

#### 3. User Interface Messages
- Updated interactive prompts to show new word ranges
- Updated log messages to reflect new limits

#### 4. Documentation
- Updated function docstrings
- Updated inline comments
- Updated type hints documentation

## Technical Details

### Word Count Logic
The application uses a two-stage process:
1. **Target Setting**: Calculates target words per section based on new limits
2. **Validation**: Ensures final reports meet minimum thresholds and don't exceed maximums
3. **Expansion**: If a report is under minimum, it triggers expansion attempts

### Section Distribution
- **Concise (1200 words)**: 2-4 sections, ~300 words each
- **Detailed (3000 words)**: 3-8 sections, ~600 words each

### Quality Control
- **Minimum threshold**: 60% of target for concise, 80% for detailed
- **Expansion attempts**: 1 for concise, 2 for detailed
- **Hard minimums**: 600 words (concise), 800 words (detailed)

## Benefits

1. **More Comprehensive Reports**: Higher word counts allow for deeper analysis
2. **Better Value**: Users get more detailed information per search
3. **Improved Quality**: More space for thorough explanations and evidence
4. **Flexible Range**: Minimum thresholds ensure substantial content while maximums prevent overwhelming output

## Usage

No changes required for users - the application will automatically:
- Apply new limits when generating reports
- Show updated word ranges in the selection menu
- Ensure all reports meet the new minimum requirements
- Maintain quality standards within the new maximums

The batch files and all other functionality remain unchanged.