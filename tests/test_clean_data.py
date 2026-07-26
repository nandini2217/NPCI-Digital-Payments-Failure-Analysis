"""
Basic tests for bank name standardization logic.
Run with: pytest tests/test_clean_data.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from clean_data import standardize_bank_name, apply_bank_aliases


def test_collapses_multiple_spaces():
    assert standardize_bank_name("Yes  Bank   Prepaid") == "Yes Bank Prepaid"

def test_fixes_corrupted_special_char():
    result = standardize_bank_name("Yes Bank ? Prepaid ? YP2")
    assert "?" not in result

def test_removes_trailing_period():
    assert standardize_bank_name("Jana Small Finance Bank Ltd.") == "Jana Small Finance Bank Ltd"

def test_normalizes_limited_to_ltd():
    result = standardize_bank_name("Equitas Small Finance Bank Limited")
    assert "Limited" not in result
    assert "Ltd" in result

def test_removes_parentheses():
    result = standardize_bank_name("Karnataka Gramin Bank (Erstwhile Pragathi)")
    assert "(" not in result and ")" not in result

def test_normalizes_casing():
    assert standardize_bank_name("bank of india") == "Bank Of India"

def test_known_alias_merges_correctly():
    standardized = standardize_bank_name("Andhra Pradesh Grameena Vikash Bank")
    result = apply_bank_aliases(standardized)
    assert result == "Andhra Pradesh Grameena Vikas Bank"

def test_unknown_bank_unaffected_by_aliases():
    result = apply_bank_aliases("State Bank Of India")
    assert result == "State Bank Of India"