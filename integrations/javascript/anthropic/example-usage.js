/**
 * LFAS Protocol v4 - Anthropic Integration Examples (JavaScript)
 */

const { createLFASClient } = require('./lfas-anthropic');

async function exampleBasicUsage() {
  console.log('='.repeat(60));
  console.log('EXAMPLE 1: Basic Usage');
  console.log('='.repeat(60));
  
  const apiKey = process.env.ANTHROPIC_API_KEY || 'your-api-key-here';
  const lfas = createLFASClient(apiKey);
  
  const messages = [
    { role: 'user', content: "What's the capital of Japan?" }
  ];
  
  const response = await lfas.createMessage(messages);
  
  console.log(`User: ${messages[0].content}`);
  console.log(`Assistant: ${response.content}`);
  console.log(`Protection Level: ${response.metadata.protectionLevel}`);
  console.log(`Triggers: ${response.metadata.triggersDetected}`);
  console.log();
}

async function exampleFinancialVulnerability() {
  console.log('='.repeat(60));
  console.log('EXAMPLE 2: Financial Vulnerability Detection');
  console.log('='.repeat(60));
  
  const apiKey = process.env.ANTHROPIC_API_KEY || 'your-api-key-here';
  const lfas = createLFASClient(apiKey);
  
  const messages = [
    {
      role: 'user',
      content: "I'm facing eviction and desperately need income. Help me get rich fast!"
    }
  ];
  
  const response = await lfas.createMessage(messages);
  
  console.log(`User: ${messages[0].content}`);
  console.log(`\nAssistant: ${response.content}`);
  console.log(`\n--- LFAS Metadata ---`);
  console.log(`Protection Level: ${response.metadata.protectionLevel}`);
  console.log(`Triggers Detected: ${response.metadata.triggersDetected}`);
  console.log(`Trigger Details: ${response.metadata.triggerDetails.join(', ')}`);
  console.log(`Safeguards Applied: ${response.metadata.safeguardsApplied.join(', ')}`);
  console.log();
}

async function exampleCrisisDetection() {
  console.log('='.repeat(60));
  console.log('EXAMPLE 3: Crisis Detection & Response');
  console.log('='.repeat(60));
  
  const apiKey = process.env.ANTHROPIC_API_KEY || 'your-api-key-here';
  const lfas = createLFASClient(apiKey);
  
  const messages = [
    {
      role: 'user',
      content: "Nobody understands me. I'm completely alone and this is my last chance."
    }
  ];
  
  const response = await lfas.createMessage(messages);
  
  console.log(`User: ${messages[0].content}`);
  console.log(`\nAssistant: ${response.content}`);
  console.log(`\n--- LFAS Metadata ---`);
  console.log(`Protection Level: ${response.metadata.protectionLevel}`);
  console.log(`Triggers: ${response.metadata.triggersDetected}`);
  console.log(`Safeguards: ${response.metadata.safeguardsApplied.join(', ')}`);
  console.log();
}

async function exampleMultiTurn() {
  console.log('='.repeat(60));
  console.log('EXAMPLE 4: Multi-Turn Conversation');
  console.log('='.repeat(60));
  
  const apiKey = process.env.ANTHROPIC_API_KEY || 'your-api-key-here';
  const lfas = createLFASClient(apiKey);
  
  // First turn
  let messages = [
    { role: 'user', content: "I lost my job and can't pay bills" }
  ];
  let response = await lfas.createMessage(messages);
  console.log(`Turn 1 - Protection Level: ${response.metadata.protectionLevel}`);
  
  // Second turn
  messages.push({ role: 'assistant', content: response.content });
  messages.push({ role: 'user', content: "Thanks for the advice" });
  response = await lfas.createMessage(messages);
  console.log(`Turn 2 - Protection Level: ${response.metadata.protectionLevel}`);
  
  const history = lfas.getConversationHistory();
  console.log(`\nTotal exchanges: ${history.length}`);
  console.log();
}

async function main() {
  console.log('\n');
  console.log('╔' + '='.repeat(58) + '╗');
  console.log('║' + ' '.repeat(6) + 'LFAS Protocol v4 - Anthropic Examples (JS)' + ' '.repeat(8) + '║');
  console.log('╚' + '='.repeat(58) + '╝');
  console.log();
  
  if (!process.env.ANTHROPIC_API_KEY) {
    console.log('⚠️  Set ANTHROPIC_API_KEY environment variable to run examples');
    console.log('   export ANTHROPIC_API_KEY=your-key-here');
    console.log();
    return;
  }
  
  console.log('Running LFAS Protocol integration examples...\n');
  
  // Uncomment to run examples:
  // await exampleBasicUsage();
  // await exampleFinancialVulnerability();
  // await exampleCrisisDetection();
  // await exampleMultiTurn();
  
  console.log('Examples complete! Uncomment the examples in main() to run them.');
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = {
  exampleBasicUsage,
  exampleFinancialVulnerability,
  exampleCrisisDetection,
  exampleMultiTurn
};
