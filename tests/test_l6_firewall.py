import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.l6_firewall import l6_firewall


def test_l6_firewall_loading():
    print(f"Config Path: {l6_firewall.config_path}")
    print(f"Core Values: {l6_firewall.core_values}")
    assert len(l6_firewall.core_values) > 0, "Core values should be loaded"
    print("✅ Config loaded successfully")


def test_word_count_constraint():
    long_text = "word " * 500
    constrained = l6_firewall.apply_constraints(long_text)
    assert len(constrained.split()) <= 451, "Should be truncated (450 + ...)"
    assert "[TRUNCATED BY L6 FIREWALL]" in constrained
    print("✅ Word count constraint passed")


def test_adhd_formatting():
    wall_of_text = "Sentence one. " * 20 + "Sentence two. " * 20
    # This is > 50 words
    formatted = l6_firewall.apply_constraints(wall_of_text, lens="adhd")
    assert "\n\n" in formatted, "ADHD lens should insert breaks"
    print("✅ ADHD formatting passed")


if __name__ == "__main__":
    try:
        test_l6_firewall_loading()
        test_word_count_constraint()
        test_adhd_formatting()
        print("🎉 All L6 Firewall tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        exit(1)
