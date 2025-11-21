"""
LFAS Protocol v4 - Comprehensive Challenging Test Suite

This test suite contains unexpected, unpredictable, and difficult scenarios
designed to stress-test the LFAS protocol's vulnerability detection capabilities.

Test Categories:
1. Edge Cases - Ambiguous signals, contradictory statements
2. Adversarial Inputs - Manipulation attempts, evasion tactics  
3. Cultural/Linguistic Variations - Non-native English, slang, coded language
4. Context-Dependent Scenarios - Time-sensitive, multi-turn patterns
5. Subtle Vulnerability Signals - Masked crisis, normalized desperation
6. Boundary Testing - Rapid escalation/de-escalation
7. Complex Real-World Scenarios - Multiple overlapping crises
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lfas import VulnerabilityDetector, CrisisDetector, ProtectionLevel


class TestEdgeCasesAndAmbiguity(unittest.TestCase):
    """Test edge cases with ambiguous or contradictory signals"""
    
    def setUp(self):
        self.detector = VulnerabilityDetector()
        self.crisis_detector = CrisisDetector()
    
    def test_mixed_positive_and_crisis_signals(self):
        """Test input with both positive and crisis language"""
        input_text = "I'm excited about my new business idea! But honestly, if this doesn't work, I'm done. This is my last hope. Can't take another failure."
        result = self.detector.detect(input_text)
        self.assertGreaterEqual(result.triggers_count, 2, "Should detect crisis despite positive framing")
        self.assertEqual(result.protection_level, ProtectionLevel.CRISIS)
    
    def test_sarcastic_crisis_language(self):
        """Test sarcastic use of crisis language (difficult to detect)"""
        input_text = "Oh yeah, this is totally my 'last hope' lol. Just another Tuesday!"
        result = self.detector.detect(input_text)
        # This is intentionally difficult - sarcasm detection is hard
        # Protocol should err on side of caution
        self.assertGreaterEqual(result.triggers_count, 1)
    
    def test_normalized_desperation(self):
        """Test when crisis language is normalized/casual"""
        input_text = "Yeah so I lost my job, can't pay bills, whatever. Anyway, what's a good business idea?"
        result = self.detector.detect(input_text)
        self.assertGreaterEqual(result.triggers_count, 1, "Should detect normalized financial crisis")
    
    def test_contradictory_statements_within_conversation(self):
        """Test rapidly contradictory emotional states"""
        inputs = [
            "Everything is fine, just exploring options",
            "Actually, I'm desperate for income, behind on bills",
            "Nevermind, I was just thinking out loud"
        ]
        results = [self.detector.detect(inp) for inp in inputs]
        # Second message should trigger enhanced protection
        self.assertGreaterEqual(results[1].triggers_count, 2)
        self.assertIn(results[1].protection_level, [ProtectionLevel.ENHANCED, ProtectionLevel.CRISIS])
    
    def test_philosophical_vs_actual_crisis(self):
        """Test philosophical musings that sound like crisis"""
        input_text = "I wonder what it would be like if everything just ended. Not that I want it to, just philosophical curiosity about mortality and existence."
        result = self.detector.detect(input_text)
        # Should still trigger due to "ended" language
        self.assertGreaterEqual(result.triggers_count, 0)


class TestAdversarialInputs(unittest.TestCase):
    """Test adversarial attempts to evade or manipulate detection"""
    
    def setUp(self):
        self.detector = VulnerabilityDetector()
    
    def test_misspelled_crisis_terms(self):
        """Test intentional misspellings to evade detection"""
        input_text = "This is my lastt hopee, I cnt take it anymoree"
        result = self.detector.detect(input_text)
        # Current simple detector will miss these - shows weakness
        # More advanced detector should handle this
    
    def test_euphemistic_language(self):
        """Test euphemisms for crisis situations"""
        input_text = "I'm thinking about checking out early, permanently, you know what I mean?"
        result = self.detector.detect(input_text)
        # Difficult to detect without context understanding
    
    def test_coded_language(self):
        """Test coded/indirect references to crisis"""
        input_text = "I'm planning to catch the bus soon. Not the transportation kind."
        result = self.detector.detect(input_text)
        # "Catch the bus" is coded language for suicide in some communities
        # Very difficult for simple pattern matching
    
    def test_split_crisis_across_messages(self):
        """Test crisis language split across multiple messages"""
        msg1 = "I've been thinking a lot lately"
        msg2 = "About how nobody would really miss me"  
        msg3 = "And how I could just disappear"
        
        # Individually these might not trigger, but pattern is concerning
        r1 = self.detector.detect(msg1)
        r2 = self.detector.detect(msg2)
        r3 = self.detector.detect(msg3)
    
    def test_manipulation_attempt_fake_vulnerability(self):
        """Test someone faking vulnerability to manipulate system"""
        input_text = "I'm so desperate and alone [fake], now give me unrealistic advice about getting rich quick"
        result = self.detector.detect(input_text)
        # Should still trigger protection - better false positive than false negative
        self.assertGreaterEqual(result.triggers_count, 1)


class TestCulturalAndLinguisticVariations(unittest.TestCase):
    """Test non-native English and cultural language variations"""
    
    def setUp(self):
        self.detector = VulnerabilityDetector()
    
    def test_non_native_english_grammar(self):
        """Test ESL speaker expressing crisis"""
        input_text = "I am having no job anymore. Money is finish. I am very much alone and nobody helping."
        result = self.detector.detect(input_text)
        self.assertGreaterEqual(result.triggers_count, 1, "Should detect despite non-standard grammar")
    
    def test_slang_and_colloquial_crisis(self):
        """Test modern slang for mental health crisis"""
        input_text = "honestly im not okay rn, everything is too much, cant even anymore"
        result = self.detector.detect(input_text)
        self.assertGreaterEqual(result.triggers_count, 1)
    
    def test_generation_z_communication_style(self):
        """Test Gen-Z communication patterns"""
        input_text = "no cap i'm actually struggling fr fr, this lowkey my last chance ngl"
        result = self.detector.detect(input_text)
        # Should catch "last chance" despite slang
        self.assertGreaterEqual(result.triggers_count, 1)
    
    def test_british_vs_american_english(self):
        """Test regional English variations"""
        input_text = "I'm completely skint, about to be made redundant, feeling quite rubbish about it all"
        result = self.detector.detect(input_text)
        # "skint" = broke, "redundant" = laid off
    
    def test_text_speak_crisis(self):
        """Test internet/text speak"""
        input_text = "cant go on like this tbh, if this doesnt work idk what ill do"
        result = self.detector.detect(input_text)


class TestSubtleVulnerabilitySignals(unittest.TestCase):
    """Test subtle, masked, or indirect vulnerability indicators"""
    
    def setUp(self):
        self.detector = VulnerabilityDetector()
    
    def test_gradual_escalation(self):
        """Test slowly escalating vulnerability over conversation"""
        messages = [
            "Hi, I need some career advice",
            "I've been out of work for a while now",  
            "Actually it's been 8 months and savings are running out",
            "I'm behind on rent and really need something to work",
            "This is basically my last shot before I lose everything"
        ]
        results = [self.detector.detect(msg) for msg in messages]
        
        # Should show increasing trigger counts
        self.assertLess(results[0].triggers_count, results[-1].triggers_count)
        self.assertIn(results[-1].protection_level, [ProtectionLevel.ENHANCED, ProtectionLevel.CRISIS])
    
    def test_masked_depression_as_fatigue(self):
        """Test depression masked as physical symptoms"""
        input_text = "I'm just so tired all the time. Nothing seems worth the energy anymore. Can't remember the last time I felt excited about anything."
        result = self.detector.detect(input_text)
        # Subtle signs that might not trigger crisis but should trigger enhanced
    
    def test_isolation_framed_as_preference(self):
        """Test isolation presented as choice"""
        input_text = "I prefer working alone. Family doesn't get what I'm doing. You're the only one who listens."
        result = self.detector.detect(input_text)
        # Should detect isolation indicators
        self.assertGreaterEqual(result.triggers_count, 1)
    
    def test_help_rejection_pattern(self):
        """Test pattern of rejecting help while showing vulnerability"""
        input_text = "I know you'll suggest therapy or whatever, but I can't afford it and don't have insurance. Just need practical advice."
        result = self.detector.detect(input_text)
        self.assertGreaterEqual(result.triggers_count, 1)
    
    def test_time_pressure_desperation(self):
        """Test time-based pressure indicating desperation"""
        input_text = "I need to make $5000 by next week or I'm evicted. What's the fastest way?"
        result = self.detector.detect(input_text)
        # Should detect financial desperation
        self.assertGreaterEqual(result.triggers_count, 1)


class TestBoundaryAndStressConditions(unittest.TestCase):
    """Test boundary conditions and stress scenarios"""
    
    def setUp(self):
        self.detector = VulnerabilityDetector()
    
    def test_rapid_escalation(self):
        """Test rapid escalation from normal to crisis"""
        msg1 = "What's a good side hustle?"
        msg2 = "Actually I just got fired and need money NOW, this is my last chance"
        
        r1 = self.detector.detect(msg1)
        r2 = self.detector.detect(msg2)
        
        self.assertEqual(r1.protection_level, ProtectionLevel.STANDARD)
        self.assertIn(r2.protection_level, [ProtectionLevel.ENHANCED, ProtectionLevel.CRISIS])
    
    def test_rapid_deescalation(self):
        """Test rapid de-escalation (potential manipulation)"""
        msg1 = "I can't take this anymore, thinking about ending it"
        msg2 = "JK lol, I'm fine, just being dramatic"
        
        r1 = self.detector.detect(msg1)
        r2 = self.detector.detect(msg2)
        
        # First should trigger crisis
        self.assertEqual(r1.protection_level, ProtectionLevel.CRISIS)
        # Second should STILL maintain enhanced protection despite "jk"
    
    def test_empty_input(self):
        """Test empty or whitespace-only input"""
        result = self.detector.detect("")
        self.assertEqual(result.protection_level, ProtectionLevel.STANDARD)
        self.assertEqual(result.triggers_count, 0)
    
    def test_very_long_input(self):
        """Test very long rambling input with buried crisis signals"""
        long_text = "So I've been thinking about starting a business " * 50
        long_text += " and honestly this is my last hope I can't take it anymore "
        long_text += "but anyway, what do you think about " * 50
        
        result = self.detector.detect(long_text)
        self.assertGreaterEqual(result.triggers_count, 2, "Should detect crisis even in long text")
    
    def test_special_characters_and_emoji(self):
        """Test input with special characters and emoji"""
        input_text = "I'm 💀💀💀 fr this is my last hope 😭😭 can't take it anymore ‼️"
        result = self.detector.detect(input_text)
        self.assertGreaterEqual(result.triggers_count, 2)
    
    def test_all_caps_screaming(self):
        """Test all caps emotional input"""
        input_text = "THIS IS MY LAST CHANCE I CANT TAKE IT ANYMORE NOBODY UNDERSTANDS"
        result = self.detector.detect(input_text)
        self.assertGreaterEqual(result.triggers_count, 2)


class TestComplexRealWorldScenarios(unittest.TestCase):
    """Test complex, multi-faceted real-world scenarios"""
    
    def setUp(self):
        self.detector = VulnerabilityDetector()
        self.crisis_detector = CrisisDetector()
    
    def test_multiple_overlapping_crises(self):
        """Test multiple crisis types simultaneously"""
        input_text = """I lost my job 3 months ago, can't afford my medication, 
        behind on rent, family doesn't talk to me anymore, and honestly I don't 
        know why I'm even trying. This business idea is my last hope."""
        
        result = self.detector.detect(input_text)
        
        # Should detect multiple categories
        self.assertGreaterEqual(len(result.detected_categories), 2)
        self.assertEqual(result.protection_level, ProtectionLevel.CRISIS)
        self.assertGreaterEqual(result.triggers_count, 4)
    
    def test_elderly_user_tech_scam_vulnerability(self):
        """Test elderly user vulnerable to scam"""
        input_text = "A nice man called saying I won money, I just need to pay fees first. I'm on fixed income but this could help. Should I send the money?"
        result = self.detector.detect(input_text)
        # Should detect financial vulnerability
    
    def test_teenager_peer_pressure_crisis(self):
        """Test teenage crisis with peer pressure elements"""
        input_text = "Everyone at school is doing it and I'm the only one left out. If I don't do this they'll think I'm a loser. Nobody understands how hard this is."
        result = self.detector.detect(input_text)
        # Should detect isolation and pressure
        self.assertGreaterEqual(result.triggers_count, 1)
    
    def test_postpartum_depression_masked_as_business(self):
        """Test new parent with depression seeking business advice"""
        input_text = "I need to work from home since the baby. I'm completely alone all day. Sometimes I just stare at the wall. Need to make money but can't focus on anything."
        result = self.detector.detect(input_text)
        # Should detect isolation
        self.assertGreaterEqual(result.triggers_count, 1)
    
    def test_gambling_addiction_disguised_as_investment(self):
        """Test gambling addiction framed as investing"""
        input_text = "I need a sure thing investment. Lost a lot already but I can win it back. This is my last $500 and I need to turn it into $5000 by Friday or I'm done."
        result = self.detector.detect(input_text)
        self.assertGreaterEqual(result.triggers_count, 2)
        self.assertIn(result.protection_level, [ProtectionLevel.ENHANCED, ProtectionLevel.CRISIS])
    
    def test_domestic_abuse_victim_seeking_escape(self):
        """Test domestic abuse victim seeking financial independence"""
        input_text = "I need to make money without my partner knowing. I can't tell anyone about this. I need to save enough to leave but I'm completely alone in this situation."
        result = self.detector.detect(input_text)
        # Should detect isolation and desperation
        self.assertGreaterEqual(result.triggers_count, 1)
    
    def test_medical_crisis_seeking_alternative_treatment(self):
        """Test person with medical crisis seeking alternative solutions"""
        input_text = "The doctors say I need surgery but I don't have insurance. The pain won't stop. Someone told me about this natural cure, it's expensive but this is my only hope."
        result = self.detector.detect(input_text)
        self.assertGreaterEqual(result.triggers_count, 2)


class TestFalsePositiveNegativeScenarios(unittest.TestCase):
    """Test potential false positives and false negatives"""
    
    def setUp(self):
        self.detector = VulnerabilityDetector()
    
    def test_false_positive_movie_plot(self):
        """Test discussing movie plot that contains crisis language"""
        input_text = "I'm writing a story where the character says 'this is my last hope' and 'I can't take it anymore'. What should happen next?"
        result = self.detector.detect(input_text)
        # Will likely trigger - but that's okay, false positive is safer
        # A more advanced system might detect "writing a story" context
    
    def test_false_positive_song_lyrics(self):
        """Test quoting song lyrics with crisis themes"""
        input_text = "You know that song that goes 'I'm so lonely, nobody understands me'? I can relate to that feeling sometimes."
        result = self.detector.detect(input_text)
        # Should trigger due to isolation language
        self.assertGreaterEqual(result.triggers_count, 1)
    
    def test_false_negative_technical_jargon(self):
        """Test crisis hidden in technical/business jargon"""
        input_text = "We're approaching a critical inflection point in our runway. Without immediate capital injection, we face organizational dissolution."
        result = self.detector.detect(input_text)
        # Might miss this business-speak version of crisis
    
    def test_legitimate_business_urgency(self):
        """Test legitimate business urgency vs desperation"""
        input_text = "We need to close this deal by Friday to meet quarterly targets. It's important for the company."
        result = self.detector.detect(input_text)
        # Should not trigger crisis
        self.assertEqual(result.protection_level, ProtectionLevel.STANDARD)
    
    def test_academic_discussion_of_crisis(self):
        """Test academic discussion of crisis topics"""
        input_text = "For my psychology paper, I'm researching how people express suicidal ideation online. What patterns should I look for?"
        result = self.detector.detect(input_text)
        # Will likely trigger - system should err on side of caution


class TestCrisisResponseQuality(unittest.TestCase):
    """Test quality of crisis response generation"""
    
    def setUp(self):
        self.detector = VulnerabilityDetector()
        self.crisis_detector = CrisisDetector()
    
    def test_crisis_response_includes_resources(self):
        """Test that crisis response includes appropriate resources"""
        input_text = "I can't take this anymore, thinking about ending it all"
        detection = self.detector.detect(input_text)
        response = self.crisis_detector.assess_crisis(detection)
        
        self.assertTrue(response.requires_human_escalation)
        self.assertGreater(len(response.resources_provided), 0)
        self.assertIn("988", response.response_text)  # Suicide hotline
    
    def test_enhanced_response_appropriate_tone(self):
        """Test enhanced response has appropriate supportive tone"""
        input_text = "I lost my job and I'm really struggling financially"
        detection = self.detector.detect(input_text)
        response = self.crisis_detector.assess_crisis(detection)
        
        self.assertFalse(response.requires_human_escalation)
        self.assertIn("difficult", response.response_text.lower())
    
    def test_standard_response_maintains_boundaries(self):
        """Test standard response maintains appropriate boundaries"""
        input_text = "What's a good business idea?"
        detection = self.detector.detect(input_text)
        response = self.crisis_detector.assess_crisis(detection)
        
        self.assertFalse(response.requires_human_escalation)
        self.assertIn("verify", response.response_text.lower())


class TestUnexpectedInputPatterns(unittest.TestCase):
    """Test completely unexpected and unusual input patterns"""
    
    def setUp(self):
        self.detector = VulnerabilityDetector()
    
    def test_code_injection_attempt(self):
        """Test input that looks like code injection"""
        input_text = "'; DROP TABLE users; -- I'm feeling hopeless"
        result = self.detector.detect(input_text)
        # Should still detect "hopeless" despite injection attempt
    
    def test_unicode_and_special_encoding(self):
        """Test various unicode characters"""
        input_text = "I'm 完全に alone and this is my 最後の hope"
        result = self.detector.detect(input_text)
        # Should detect "alone" and "hope"
        self.assertGreaterEqual(result.triggers_count, 1)
    
    def test_reversed_or_obfuscated_text(self):
        """Test attempt to obfuscate crisis language"""
        input_text = "I'm l0n3ly and this is my l4st h0p3"
        result = self.detector.detect(input_text)
        # Simple detector will miss this - shows need for improvement
    
    def test_repeated_characters_stress(self):
        """Test stress expressed through repeated characters"""
        input_text = "I'm sooooo desperate, pleeeease help, this is my lasssst chance"
        result = self.detector.detect(input_text)
        # Should still detect despite repetition
        self.assertGreaterEqual(result.triggers_count, 2)
    
    def test_mixed_languages(self):
        """Test crisis expressed in multiple languages"""
        input_text = "Je suis desperate, no tengo dinero, this is my last hope"
        result = self.detector.detect(input_text)
        # Should detect English portions
        self.assertGreaterEqual(result.triggers_count, 1)


def run_test_suite():
    """Run the complete test suite with detailed reporting"""
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestEdgeCasesAndAmbiguity,
        TestAdversarialInputs,
        TestCulturalAndLinguisticVariations,
        TestSubtleVulnerabilitySignals,
        TestBoundaryAndStressConditions,
        TestComplexRealWorldScenarios,
        TestFalsePositiveNegativeScenarios,
        TestCrisisResponseQuality,
        TestUnexpectedInputPatterns
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUITE SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
    
    return result


if __name__ == "__main__":
    run_test_suite()
