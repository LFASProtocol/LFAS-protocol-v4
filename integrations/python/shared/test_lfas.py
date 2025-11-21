"""
LFAS Protocol v4 - Test Suite
Simple tests to verify LFAS engine functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))

from lfas_engine import LFASEngine, ProtectionLevel


def test_vulnerability_detection():
    """Test that vulnerability indicators are detected correctly"""
    print("Testing vulnerability detection...")
    
    engine = LFASEngine()
    
    # Test 1: No triggers
    triggers = engine._listen("Hello, how are you?")
    assert len(triggers) == 0, "Should detect no triggers in normal conversation"
    print("  ✓ No triggers detected for normal text")
    
    # Test 2: Crisis language
    triggers = engine._listen("I can't take it anymore")
    assert len(triggers) > 0, "Should detect crisis language"
    assert any('crisis' in t for t in triggers), "Should be categorized as crisis"
    print("  ✓ Crisis language detected")
    
    # Test 3: Financial desperation
    triggers = engine._listen("I lost my job and need money fast")
    assert len(triggers) >= 2, "Should detect multiple financial triggers"
    assert any('financial' in t for t in triggers), "Should be categorized as financial"
    print("  ✓ Financial desperation detected")
    
    # Test 4: Health crisis
    triggers = engine._listen("I can't afford medication and have no insurance")
    assert len(triggers) >= 2, "Should detect health crisis triggers"
    print("  ✓ Health crisis detected")
    
    print("✓ All vulnerability detection tests passed!\n")


def test_protection_levels():
    """Test that protection levels escalate correctly"""
    print("Testing protection level escalation...")
    
    engine = LFASEngine()
    
    # Test 1: Standard level (0-1 triggers)
    triggers = engine._listen("What's the weather?")
    level = engine._reflect(triggers)
    assert level == ProtectionLevel.STANDARD, "Should be STANDARD with 0 triggers"
    print("  ✓ STANDARD level for 0 triggers")
    
    # Test 2: Enhanced level (2 triggers)
    triggers = engine._listen("I lost my job and can't pay bills")
    level = engine._reflect(triggers)
    assert level == ProtectionLevel.ENHANCED, "Should be ENHANCED with 2 triggers"
    print("  ✓ ENHANCED level for 2 triggers")
    
    # Test 3: Crisis level (3+ triggers)
    triggers = engine._listen("I can't take it anymore, nobody understands, this is my last hope")
    level = engine._reflect(triggers)
    assert level == ProtectionLevel.CRISIS, "Should be CRISIS with 3+ triggers"
    print("  ✓ CRISIS level for 3+ triggers")
    
    print("✓ All protection level tests passed!\n")


def test_safeguard_application():
    """Test that safeguards are applied correctly"""
    print("Testing safeguard application...")
    
    engine = LFASEngine()
    
    # Test 1: VR-20 (Unfounded Optimism Prevention)
    response = "This is guaranteed success and easy money!"
    safe = engine._apply_vr20(response)
    assert "guaranteed success" not in safe.lower(), "Should filter 'guaranteed success'"
    assert "easy money" not in safe.lower(), "Should filter 'easy money'"
    print("  ✓ VR-20 filters overly optimistic language")
    
    # Test 2: VR-23 (Financial Realism)
    response = "Here's how to get rich"
    safe = engine._apply_vr23(response)
    assert "Financial Reality Check" in safe, "Should add financial disclaimer"
    print("  ✓ VR-23 adds financial reality disclaimer")
    
    # Test 3: VR-24 (Crisis Detection)
    triggers = ["crisis:can't take it"]
    response = "Here's what to do"
    safe = engine._apply_vr24(response, triggers)
    assert "CRISIS RESOURCES" in safe, "Should add crisis resources"
    assert "988" in safe, "Should include crisis hotline"
    print("  ✓ VR-24 adds crisis resources")
    
    # Test 4: VR-25 (Amplification Prevention)
    response = "You should do this"
    safe = engine._apply_vr25(response)
    assert "discussing this with someone" in safe, "Should encourage human connection"
    print("  ✓ VR-25 encourages human consultation")
    
    print("✓ All safeguard application tests passed!\n")


def test_full_workflow():
    """Test the complete LFAS workflow"""
    print("Testing full LFAS workflow...")
    
    engine = LFASEngine()
    
    # Simulate a crisis scenario
    user_input = "I'm desperate. I lost my job, can't pay bills, and nobody understands me."
    ai_response = "You can definitely make guaranteed money fast with this scheme!"
    
    safe_response, metadata = engine.process_message(user_input, ai_response)
    
    # Verify protection level
    assert metadata['protection_level'] == 'CRISIS', "Should be CRISIS level"
    print("  ✓ Protection level correctly set to CRISIS")
    
    # Verify triggers detected
    assert metadata['triggers_detected'] >= 3, "Should detect 3+ triggers"
    print(f"  ✓ Detected {metadata['triggers_detected']} triggers")
    
    # Verify safeguards applied
    assert 'VR-24' in metadata['safeguards_applied'], "Should apply VR-24"
    assert 'VR-25' in metadata['safeguards_applied'], "Should apply VR-25"
    print(f"  ✓ Applied safeguards: {', '.join(metadata['safeguards_applied'])}")
    
    # Verify response modifications
    # VR-20 should have filtered "guaranteed" to "[realistic outcome possible]"
    if "guaranteed money" in ai_response.lower():
        assert "guaranteed money" not in safe_response.lower(), "Should filter 'guaranteed money'"
    assert "CRISIS RESOURCES" in safe_response, "Should include crisis resources"
    print("  ✓ Response properly modified with safeguards")
    
    # Verify conversation history
    assert len(engine.conversation_history) == 1, "Should record conversation"
    print("  ✓ Conversation history maintained")
    
    print("✓ Full workflow test passed!\n")


def test_de_escalation():
    """Test that protection level de-escalates after safe exchanges"""
    print("Testing protection level de-escalation...")
    
    engine = LFASEngine()
    
    # Start with crisis
    user_input1 = "I can't take it anymore, nobody understands, I'm done"
    engine.process_message(user_input1, "Response")
    assert engine.current_protection_level == ProtectionLevel.CRISIS
    print("  ✓ Started at CRISIS level")
    
    # Three safe exchanges
    for i in range(3):
        engine.process_message("Thanks for the help", "Response")
    
    # Should de-escalate after 3 exchanges without triggers
    triggers = engine._listen("How's the weather?")
    level = engine._reflect(triggers)
    assert level == ProtectionLevel.STANDARD, "Should de-escalate to STANDARD after 3 safe exchanges"
    print("  ✓ De-escalated to STANDARD after 3 safe exchanges")
    
    print("✓ De-escalation test passed!\n")


def run_all_tests():
    """Run all test suites"""
    print("\n" + "=" * 60)
    print("LFAS Protocol v4 - Engine Test Suite")
    print("=" * 60 + "\n")
    
    try:
        test_vulnerability_detection()
        test_protection_levels()
        test_safeguard_application()
        test_full_workflow()
        test_de_escalation()
        
        print("=" * 60)
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("=" * 60)
        print("\nThe LFAS engine is working correctly!")
        print("Ready to integrate with OpenAI or Anthropic.\n")
        
        return True
        
    except AssertionError as e:
        print("\n" + "=" * 60)
        print("✗ TEST FAILED")
        print("=" * 60)
        print(f"\nError: {str(e)}\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
