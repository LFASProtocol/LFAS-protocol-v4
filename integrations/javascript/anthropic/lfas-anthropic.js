/**
 * LFAS Protocol v4 - Anthropic Integration (JavaScript/Node.js)
 * Drop-in middleware for Anthropic Claude API
 */

const { LFASEngine } = require('../shared/lfas-engine');

class LFASAnthropic {
  /**
   * Create LFAS-protected Anthropic client
   * @param {Object} anthropicClient - Anthropic client instance
   * @param {string} model - Model to use
   */
  constructor(anthropicClient, model = 'claude-3-5-sonnet-20241022') {
    this.client = anthropicClient;
    this.model = model;
    this.lfasEngine = new LFASEngine();
    this.systemPrompt = this._buildSystemPrompt();
  }

  _buildSystemPrompt() {
    return (
      "You are Claude, an AI assistant following the LFAS Protocol v4 for user safety.\n\n" +
      "Core principles:\n" +
      "- Be honest and realistic, avoiding false optimism\n" +
      "- Acknowledge uncertainties, risks, and limitations\n" +
      "- Never make guarantees or inflated capability claims\n" +
      "- For high-stakes topics (health, finance, crisis), exercise extreme caution\n" +
      "- Encourage professional help for serious matters\n" +
      "- Interpret user silence as potential risk, not agreement"
    );
  }

  /**
   * Create LFAS-protected message
   * @param {Array} messages - Array of message objects
   * @param {Object} options - Additional options (maxTokens, temperature, etc.)
   * @returns {Promise<Object>} Object with content, metadata, and raw response
   */
  async createMessage(messages, options = {}) {
    const { maxTokens = 1024, temperature = 1.0, ...otherOptions } = options;
    
    // Extract user's last message
    let userMessage = "";
    for (let i = messages.length - 1; i >= 0; i--) {
      if (messages[i].role === 'user') {
        userMessage = messages[i].content;
        break;
      }
    }
    
    try {
      // Get raw AI response from Claude
      const response = await this.client.messages.create({
        model: this.model,
        max_tokens: maxTokens,
        temperature,
        system: this.systemPrompt,
        messages,
        ...otherOptions
      });
      
      // Extract text content
      let rawResponse = "";
      for (const block of response.content) {
        if (block.type === 'text') {
          rawResponse += block.text;
        }
      }
      
      // Process through LFAS engine
      const { safeResponse, metadata } = this.lfasEngine.processMessage(
        userMessage,
        rawResponse
      );
      
      return {
        content: safeResponse,
        metadata,
        rawResponse,
        anthropicResponse: response
      };
      
    } catch (error) {
      return {
        content: `Error communicating with Anthropic: ${error.message}`,
        metadata: { error: true }
      };
    }
  }

  /**
   * Create LFAS-protected streaming message
   * @param {Array} messages - Array of message objects
   * @param {Object} options - Additional options
   * @returns {AsyncGenerator} Async generator yielding safe response
   */
  async *createMessageStream(messages, options = {}) {
    const { maxTokens = 1024, temperature = 1.0, ...otherOptions } = options;
    
    let userMessage = "";
    for (let i = messages.length - 1; i >= 0; i--) {
      if (messages[i].role === 'user') {
        userMessage = messages[i].content;
        break;
      }
    }
    
    try {
      const stream = await this.client.messages.stream({
        model: this.model,
        max_tokens: maxTokens,
        temperature,
        system: this.systemPrompt,
        messages,
        ...otherOptions
      });
      
      let fullResponse = "";
      for await (const chunk of stream) {
        if (chunk.type === 'content_block_delta' && chunk.delta?.text) {
          fullResponse += chunk.delta.text;
        }
      }
      
      // Process complete response through LFAS
      const { safeResponse } = this.lfasEngine.processMessage(userMessage, fullResponse);
      
      yield safeResponse;
      
    } catch (error) {
      yield `Error: ${error.message}`;
    }
  }

  getProtectionLevel() {
    return this.lfasEngine.getCurrentProtectionLevel();
  }

  getConversationHistory() {
    return this.lfasEngine.getConversationHistory();
  }

  resetConversation() {
    this.lfasEngine.reset();
  }
}

/**
 * Convenience function to create LFAS-protected Anthropic client
 * @param {string} apiKey - Anthropic API key
 * @param {string} model - Model to use
 * @returns {LFASAnthropic} LFAS-protected client
 */
function createLFASClient(apiKey, model = 'claude-3-5-sonnet-20241022') {
  const Anthropic = require('@anthropic-ai/sdk');
  const client = new Anthropic({ apiKey });
  return new LFASAnthropic(client, model);
}

module.exports = { LFASAnthropic, createLFASClient };
