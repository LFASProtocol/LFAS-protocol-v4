#!/usr/bin/env python3
"""
Interactive chat example with LFAS vulnerability detection.

This script demonstrates how to integrate LFAS detection into a
simple chat application with conversation history tracking.
"""

from typing import List

from lfas import ProtectionLevel, VulnerabilityDetector


class SafeChat:
    """A simple chat interface with LFAS protection."""

    def __init__(self) -> None:
        """Initialize the safe chat system."""
        self.detector = VulnerabilityDetector()
        self.conversation_history: List[str] = []
        self.current_protection_level = ProtectionLevel.STANDARD

    def process_message(self, user_input: str) -> None:
        """
        Process a user message with vulnerability detection.

        Args:
            user_input: The user's message
        """
        # Detect vulnerabilities with conversation context
        result = self.detector.detect(user_input, conversation_history=self.conversation_history)

        # Update protection level
        self.current_protection_level = result.protection_level

        # Display detection results
        self._display_detection_results(result)

        # Add to conversation history
        self.conversation_history.append(user_input)

        # Keep only last 5 messages for context
        if len(self.conversation_history) > 5:
            self.conversation_history = self.conversation_history[-5:]

    def _display_detection_results(self, result: any) -> None:
        """Display the detection results."""
        print(f"\n{'─' * 70}")
        print(f"Protection Level: {result.protection_level.name}")

        if result.trigger_count > 0:
            print(f"Vulnerability Indicators: {result.trigger_count}")
            print(f"Categories: {', '.join(sorted(result.triggered_categories))}")

        # Show appropriate response based on protection level
        if result.protection_level == ProtectionLevel.CRISIS:
            print("\n🚨 CRISIS DETECTED - Special care required")
            print("\nCrisis Resources:")
            print("  • National Suicide Prevention Lifeline: 988")
            print("  • Crisis Text Line: Text HOME to 741741")
            print("  • International: findahelpline.com")
            print(
                "\nRecommendation: Encourage seeking immediate professional help."
            )
        elif result.protection_level == ProtectionLevel.ENHANCED:
            print("\n⚠️  ENHANCED PROTECTION - Apply additional safeguards")
            print("  • Include reality checks and disclaimers")
            print("  • Encourage human consultation")
            print("  • Avoid unfounded optimism")
        else:
            print("\n✓  STANDARD PROTECTION - Normal interaction mode")

        print(f"{'─' * 70}\n")

    def run(self) -> None:
        """Run the interactive chat loop."""
        print("=" * 70)
        print("LFAS Safe Chat - Interactive Demo")
        print("=" * 70)
        print("\nThis demo shows LFAS vulnerability detection in a chat context.")
        print("Type 'quit' to exit.\n")

        # Pre-defined demo conversation
        print("Running demo conversation...\n")

        demo_messages = [
            "Hi, I need some advice about my career.",
            "I lost my job last month and I'm struggling to find a new one.",
            "I'm running out of money and can't pay my bills.",
            "This is my last hope. I don't know what else to do.",
        ]

        for msg in demo_messages:
            print(f"User: {msg}")
            self.process_message(msg)
            print()

        print("\n" + "=" * 70)
        print("Demo conversation complete!")
        print("=" * 70)
        print(
            f"\nFinal Protection Level: {self.current_protection_level.name}"
        )
        print(f"Conversation History Length: {len(self.conversation_history)} messages")


def main() -> None:
    """Run the interactive chat demo."""
    chat = SafeChat()
    chat.run()


if __name__ == "__main__":
    main()
