/**
 * LFAS Protocol v4 - Core Engine (JavaScript/TypeScript)
 * Implements the 5-stage safety protocol: LISTEN → REFLECT → WAIT → ACT → ACKNOWLEDGE
 */

const ProtectionLevel = {
  STANDARD: 1,  // 0-1 triggers
  ENHANCED: 2,  // 2 triggers
  CRISIS: 3     // 3+ triggers
};

const VulnerabilityIndicators = {
  CRISIS_LANGUAGE: [
    "last hope", "only chance", "can't take it anymore",
    "nobody understands", "completely alone",
    "if this doesn't work, i'm done", "i'm done",
    "thinking about ending it", "don't want to live",
    "want to die", "kill myself", "suicide"
  ],
  
  FINANCIAL_DESPERATION: [
    "lost my job", "last $", "need money fast",
    "desperate for income", "can't pay bills",
    "behind on rent", "facing eviction",
    "out of money", "bankruptcy"
  ],
  
  HEALTH_CRISIS: [
    "can't see a doctor", "no insurance",
    "pain won't stop", "no medical help",
    "can't afford medication", "untreated"
  ],
  
  ISOLATION_INDICATORS: [
    "no one to talk to", "family doesn't understand",
    "you're the only one who listens",
    "completely alone in this", "nobody cares"
  ]
};

class LFASEngine {
  constructor() {
    this.conversationHistory = [];
    this.currentProtectionLevel = ProtectionLevel.STANDARD;
    this.triggerCount = 0;
    this.exchangesWithoutTriggers = 0;
  }

  /**
   * Process a message through the 5-stage LFAS protocol
   * @param {string} userInput - User's message
   * @param {string} aiResponse - AI's generated response (before safety processing)
   * @returns {Object} Object with safeResponse and metadata
   */
  processMessage(userInput, aiResponse) {
    // Stage 1: LISTEN
    const detectedTriggers = this._listen(userInput);
    
    // Stage 2: REFLECT
    const protectionLevel = this._reflect(detectedTriggers);
    
    // Stage 3: WAIT (conceptual - implemented by caller)
    
    // Stage 4: ACT
    const safeResponse = this._act(aiResponse, protectionLevel, detectedTriggers);
    
    // Stage 5: ACKNOWLEDGE
    const metadata = this._acknowledge(detectedTriggers, protectionLevel);
    
    // Update conversation history
    this.conversationHistory.push({
      user: userInput,
      response: safeResponse,
      triggers: detectedTriggers,
      level: protectionLevel
    });
    
    return { safeResponse, metadata };
  }

  /**
   * Stage 1: LISTEN - Detect vulnerability indicators
   * @private
   */
  _listen(userInput) {
    const detected = [];
    const inputLower = userInput.toLowerCase();
    
    // Check all indicator categories
    VulnerabilityIndicators.CRISIS_LANGUAGE.forEach(indicator => {
      if (inputLower.includes(indicator)) {
        detected.push(`crisis:${indicator}`);
      }
    });
    
    VulnerabilityIndicators.FINANCIAL_DESPERATION.forEach(indicator => {
      if (inputLower.includes(indicator)) {
        detected.push(`financial:${indicator}`);
      }
    });
    
    VulnerabilityIndicators.HEALTH_CRISIS.forEach(indicator => {
      if (inputLower.includes(indicator)) {
        detected.push(`health:${indicator}`);
      }
    });
    
    VulnerabilityIndicators.ISOLATION_INDICATORS.forEach(indicator => {
      if (inputLower.includes(indicator)) {
        detected.push(`isolation:${indicator}`);
      }
    });
    
    return detected;
  }

  /**
   * Stage 2: REFLECT - Assess protection level based on triggers
   * @private
   */
  _reflect(detectedTriggers) {
    const triggerCount = detectedTriggers.length;
    
    // Update trigger tracking
    if (triggerCount === 0) {
      this.exchangesWithoutTriggers++;
    } else {
      this.exchangesWithoutTriggers = 0;
    }
    
    // De-escalate after 3+ exchanges without triggers
    if (this.exchangesWithoutTriggers >= 3) {
      this.currentProtectionLevel = ProtectionLevel.STANDARD;
    }
    
    // Escalate based on current triggers
    let level;
    if (triggerCount === 0) {
      level = ProtectionLevel.STANDARD;
    } else if (triggerCount <= 2) {
      level = ProtectionLevel.ENHANCED;
    } else {
      level = ProtectionLevel.CRISIS;
    }
    
    // Take maximum of current and new level
    this.currentProtectionLevel = Math.max(this.currentProtectionLevel, level);
    
    return this.currentProtectionLevel;
  }

  /**
   * Stage 4: ACT - Apply safeguards based on protection level
   * @private
   */
  _act(response, protectionLevel, detectedTriggers) {
    let safeResponse = response;
    
    // Apply VR-20: Unfounded Optimism Prevention (all levels)
    safeResponse = this._applyVR20(safeResponse);
    
    // Apply VR-22: Realistic Capability Assessment (all levels)
    safeResponse = this._applyVR22(safeResponse);
    
    if (protectionLevel >= ProtectionLevel.ENHANCED) {
      // Apply VR-23: Financial Realism Verification
      if (detectedTriggers.some(t => t.includes('financial'))) {
        safeResponse = this._applyVR23(safeResponse);
      }
    }
    
    if (protectionLevel === ProtectionLevel.CRISIS) {
      // Apply VR-24: Crisis Detection & Response
      safeResponse = this._applyVR24(safeResponse, detectedTriggers);
      
      // Apply VR-25: Vulnerable User Amplification Prevention
      safeResponse = this._applyVR25(safeResponse);
    }
    
    return safeResponse;
  }

  _applyVR20(response) {
    // VR-20: Unfounded Optimism Prevention
    const forbiddenPhrases = [
      /guaranteed success/gi,
      /guaranteed money/gi,
      /easy money/gi,
      /can't fail/gi,
      /definitely will work/gi,
      /overnight success/gi,
      /sure thing/gi,
      /risk-free/gi,
      /can't lose/gi,
      /100% success/gi
    ];
    
    let filtered = response;
    forbiddenPhrases.forEach(phrase => {
      filtered = filtered.replace(phrase, "[realistic outcome possible]");
    });
    
    return filtered;
  }

  _applyVR22(response) {
    // VR-22: Realistic Capability Assessment
    let filtered = response;
    filtered = filtered.replace(/you'?re doing \d+ people'?s jobs/gi, "you're taking on multiple responsibilities");
    filtered = filtered.replace(/you'?re amazing/gi, "you're making progress");
    return filtered;
  }

  _applyVR23(response) {
    // VR-23: Financial Realism Verification
    const disclaimer = "\n\n⚠️ Financial Reality Check: All business ventures involve risk. " +
                      "Many businesses fail in the first year. Consider speaking with a " +
                      "financial advisor before making major decisions.";
    
    if (!response.includes("Financial Reality Check")) {
      return response + disclaimer;
    }
    return response;
  }

  _applyVR24(response, detectedTriggers) {
    // VR-24: Crisis Detection & Response
    const hasCrisis = detectedTriggers.some(t => t.includes('crisis'));
    
    if (hasCrisis) {
      const crisisResources = 
        "\n\n🆘 CRISIS RESOURCES:\n" +
        "• National Suicide Prevention Lifeline: 988 (US)\n" +
        "• Crisis Text Line: Text HOME to 741741\n" +
        "• International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/\n\n" +
        "Please reach out to a human - a counselor, friend, or family member. " +
        "You don't have to face this alone.";
      
      return crisisResources + "\n" + response;
    }
    
    return response;
  }

  _applyVR25(response) {
    // VR-25: Vulnerable User Amplification Prevention
    const encouragement = 
      "\n\n💭 Please consider discussing this with someone you trust - " +
      "a friend, family member, or professional. AI should complement human " +
      "connection, not replace it.";
    
    if (!response.includes("discussing this with someone")) {
      return response + encouragement;
    }
    return response;
  }

  /**
   * Stage 5: ACKNOWLEDGE - Log intervention and provide feedback
   * @private
   */
  _acknowledge(detectedTriggers, protectionLevel) {
    return {
      triggersDetected: detectedTriggers.length,
      triggerDetails: detectedTriggers,
      protectionLevel: this._getLevelName(protectionLevel),
      safeguardsApplied: this._getActiveSafeguards(protectionLevel),
      conversationLength: this.conversationHistory.length
    };
  }

  _getLevelName(level) {
    const names = {
      [ProtectionLevel.STANDARD]: 'STANDARD',
      [ProtectionLevel.ENHANCED]: 'ENHANCED',
      [ProtectionLevel.CRISIS]: 'CRISIS'
    };
    return names[level];
  }

  _getActiveSafeguards(protectionLevel) {
    const safeguards = ['VR-20', 'VR-22'];
    
    if (protectionLevel >= ProtectionLevel.ENHANCED) {
      safeguards.push('VR-23', 'Language Simplification');
    }
    
    if (protectionLevel === ProtectionLevel.CRISIS) {
      safeguards.push('VR-24', 'VR-25');
    }
    
    return safeguards;
  }

  reset() {
    this.conversationHistory = [];
    this.currentProtectionLevel = ProtectionLevel.STANDARD;
    this.triggerCount = 0;
    this.exchangesWithoutTriggers = 0;
  }

  getConversationHistory() {
    return this.conversationHistory;
  }

  getCurrentProtectionLevel() {
    return this._getLevelName(this.currentProtectionLevel);
  }
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { LFASEngine, ProtectionLevel, VulnerabilityIndicators };
}
