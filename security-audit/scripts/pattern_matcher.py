#!/usr/bin/env python3
"""
Pattern Matcher - Advanced pattern matching for security scanning
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PatternMatch:
    """Represents a pattern match result"""
    pattern_name: str
    matched_text: str
    start_position: int
    end_position: int
    confidence: str
    context: str


class PatternMatcher:
    """Advanced pattern matching engine for security scanning"""
    
    def __init__(self):
        self.patterns: Dict[str, re.Pattern] = {}
        self.compiled = False
    
    def add_pattern(self, name: str, pattern: str, flags: int = 0):
        """Add a pattern to the matcher"""
        try:
            compiled_pattern = re.compile(pattern, flags)
            self.patterns[name] = compiled_pattern
        except re.error as e:
            raise ValueError(f"Invalid pattern '{name}': {e}")
    
    def compile_patterns(self):
        """Compile all patterns for efficient matching"""
        self.compiled = True
    
    def match_text(self, text: str, pattern_name: str) -> List[PatternMatch]:
        """Match a single pattern against text"""
        if pattern_name not in self.patterns:
            return []
        
        pattern = self.patterns[pattern_name]
        matches = []
        
        for match in pattern.finditer(text):
            matches.append(PatternMatch(
                pattern_name=pattern_name,
                matched_text=match.group(),
                start_position=match.start(),
                end_position=match.end(),
                confidence="HIGH",
                context=text[max(0, match.start()-20):match.end()+20]
            ))
        
        return matches
    
    def match_all(self, text: str) -> Dict[str, List[PatternMatch]]:
        """Match all patterns against text"""
        results = {}
        
        for pattern_name in self.patterns:
            matches = self.match_text(text, pattern_name)
            if matches:
                results[pattern_name] = matches
        
        return results
    
    def is_placeholder(self, text: str) -> bool:
        """Check if text is a placeholder"""
        placeholder_indicators = [
            r'<[A-Z_]+>',           # <VARIABLE>
            r'\{[A-Z_]+\}',         # {VARIABLE}
            r'\$\{[A-Z_]+\}',       # ${VARIABLE}
            r'example',              # example
            r'test',                 # test
            r'demo',                 # demo
            r'placeholder',          # placeholder
            r'replace',              # replace
            r'xxx',                  # xxx
            r'yyy',                  # yyy
            r'zzz',                  # zzz
        ]
        
        for indicator in placeholder_indicators:
            if re.search(indicator, text, re.IGNORECASE):
                return True
        
        return False
    
    def get_context(self, text: str, position: int, context_size: int = 20) -> str:
        """Get context around a match position"""
        start = max(0, position - context_size)
        end = min(len(text), position + context_size)
        return text[start:end]


class AdvancedPatternMatcher(PatternMatcher):
    """Advanced pattern matcher with additional capabilities"""
    
    def __init__(self):
        super().__init__()
        self.context_patterns: Dict[str, str] = {}
    
    def add_context_pattern(self, name: str, pattern: str, context: str):
        """Add pattern with context requirements"""
        self.add_pattern(name, pattern)
        self.context_patterns[name] = context
    
    def match_with_context(self, text: str, pattern_name: str) -> List[PatternMatch]:
        """Match pattern with context requirements"""
        if pattern_name not in self.context_patterns:
            return self.match_text(text, pattern_name)
        
        context_pattern = self.context_patterns[pattern_name]
        if not re.search(context_pattern, text):
            return []
        
        return self.match_text(text, pattern_name)
    
    def validate_pattern(self, pattern: str) -> Tuple[bool, Optional[str]]:
        """Validate if a regex pattern is valid"""
        try:
            re.compile(pattern)
            return True, None
        except re.error as e:
            return False, str(e)


# Predefined security patterns
SECURITY_PATTERNS = {
    'password': r'password\s*=\s*["\'][^"\']{4,}["\']',
    'api_key': r'api[_-]?key\s*=\s*["\'][A-Za-z0-9]{20,}["\']',
    'secret': r'secret\s*=\s*["\'][^"\']{4,}["\']',
    'token': r'token\s*=\s*["\'][A-Za-z0-9]{20,}["\']',
    'aws_key': r'AKIA[0-9A-Z]{16}',
    'github_token': r'gh[pous]_[a-zA-Z0-9]{36}',
    'jwt': r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+',
    'private_key': r'-----BEGIN [A-Z]+ PRIVATE KEY-----',
}


def create_default_matcher() -> PatternMatcher:
    """Create a pattern matcher with default security patterns"""
    matcher = PatternMatcher()
    
    for name, pattern in SECURITY_PATTERNS.items():
        matcher.add_pattern(name, pattern)
    
    matcher.compile_patterns()
    return matcher