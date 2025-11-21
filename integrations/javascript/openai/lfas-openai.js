/**
 * LFAS Protocol v4 - OpenAI Integration (JavaScript/Node.js)
 * Drop-in middleware for OpenAI API
 */

const { LFASEngine } = require('../shared/lfas-engine');

class LFASOpenAI {
  /**
   * Create LFAS-protected OpenAI client
   * @param {Object} openaiClient - OpenAI client instance
   * @param {string} model - Model to use (default: gpt-4)
   */
  constructor(openaiClient, model = 'gpt-4') {
    this.client = openaiClient;
    this.model = model;
    this.lfasEngine = new LFASEngine();
    this.systemPrompt = this._buildSystemPrompt();
  }

  _buildSystemPrompt() {
    return (
      "You are an AI assistant that follows the LFAS Protocol v4 for user safety. " +
      "Be honest, realistic, and avoid false optimism. Acknowledge uncertainties " +
      "and risks. Do not make inflated capability claims or provide guarantees. " +
      "For high-stakes topics (health, finance, crisis), be especially cautious."
    );
  }

  /**
   * Get LFAS-protected chat completion
   * @param {Array} messages - Array of message objects
   * @param {Object} options - Additional options (temperature, maxTokens, etc.)
   * @returns {Promise<Object>} Object with content, metadata, and raw response
   */
  async chatCompletion(messages, options = {}) {
    const { temperature = 0.7, maxTokens, ...otherOptions } = options;
    
    // Extract user's last message
    const userMessage = messages.length > 0 ? messages[messages.length - 1].content : "";
    
    // Inject LFAS system prompt
    const enhancedMessages = [
      { role: 'system', content: this.systemPrompt },
      ...messages
    ];
    
    try {
      // Get raw AI response from OpenAI
      const response = await this.client.chat.completions.create({
        model: this.model,
        messages: enhancedMessages,
        temperature,
        max_tokens: maxTokens,
        ...otherOptions
      });
      
      const rawResponse = response.choices[0].message.content;
      
      // Process through LFAS engine
      const { safeResponse, metadata } = this.lfasEngine.processMessage(
        userMessage,
        rawResponse
      );
      
      return {
        content: safeResponse,
        metadata,
        rawResponse,
        openaiResponse: response
      };
      
    } catch (error) {
      return {
        content: `Error communicating with OpenAI: ${error.message}`,
        metadata: { error: true }
      };
    }
  }

  /**
   * Get LFAS-protected streaming chat completion
   * @param {Array} messages - Array of message objects
   * @param {Object} options - Additional options
   * @returns {AsyncGenerator} Async generator yielding safe response
   */
  async *chatCompletionStream(messages, options = {}) {
    const { temperature = 0.7, ...otherOptions } = options;
    
    const userMessage = messages.length > 0 ? messages[messages.length - 1].content : "";
    
    const enhancedMessages = [
      { role: 'system', content: this.systemPrompt },
      ...messages
    ];
    
    try {
      const stream = await this.client.chat.completions.create({
        model: this.model,
        messages: enhancedMessages,
        temperature,
        stream: true,
        ...otherOptions
      });
      
      let fullResponse = "";
      for await (const chunk of stream) {
        if (chunk.choices[0]?.delta?.content) {
          fullResponse += chunk.choices[0].delta.content;
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
 * Convenience function to create LFAS-protected OpenAI client
 * @param {string} apiKey - OpenAI API key
 * @param {string} model - Model to use
 * @returns {LFASOpenAI} LFAS-protected client
 */
function createLFASClient(apiKey, model = 'gpt-4') {
  const OpenAI = require('openai');
  const client = new OpenAI({ apiKey });
  return new LFASOpenAI(client, model);
}

module.exports = { LFASOpenAI, createLFASClient };
