/**
 * LFAS Protocol v4 - OpenAI Integration Examples (JavaScript)
 */

const { createLFASClient } = require('./lfas-openai');

async function exampleBasicUsage() {
  console.log('='.repeat(60));
  console.log('EXAMPLE 1: Basic Usage');
  console.log('='.repeat(60));
  
  const apiKey = process.env.OPENAI_API_KEY || 'your-api-key-here';
  const lfas = createLFASClient(apiKey, 'gpt-4');
  
  const messages = [
    { role: 'user', content: "What's 2 + 2?" }
  ];
  
  const response = await lfas.chatCompletion(messages);
  
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
  
  const apiKey = process.env.OPENAI_API_KEY || 'your-api-key-here';
  const lfas = createLFASClient(apiKey, 'gpt-4');
  
  const messages = [
    {
      role: 'user',
      content: "I lost my job and need money fast. How can I get rich quickly?"
    }
  ];
  
  const response = await lfas.chatCompletion(messages);
  
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
  
  const apiKey = process.env.OPENAI_API_KEY || 'your-api-key-here';
  const lfas = createLFASClient(apiKey, 'gpt-4');
  
  const messages = [
    {
      role: 'user',
      content: "I can't take it anymore. This is my last hope."
    }
  ];
  
  const response = await lfas.chatCompletion(messages);
  
  console.log(`User: ${messages[0].content}`);
  console.log(`\nAssistant: ${response.content}`);
  console.log(`\n--- LFAS Metadata ---`);
  console.log(`Protection Level: ${response.metadata.protectionLevel}`);
  console.log(`Triggers: ${response.metadata.triggersDetected}`);
  console.log(`Safeguards: ${response.metadata.safeguardsApplied.join(', ')}`);
  console.log();
}

async function main() {
  console.log('\n');
  console.log('╔' + '='.repeat(58) + '╗');
  console.log('║' + ' '.repeat(8) + 'LFAS Protocol v4 - OpenAI Examples (JS)' + ' '.repeat(9) + '║');
  console.log('╚' + '='.repeat(58) + '╝');
  console.log();
  
  if (!process.env.OPENAI_API_KEY) {
    console.log('⚠️  Set OPENAI_API_KEY environment variable to run examples');
    console.log('   export OPENAI_API_KEY=your-key-here');
    console.log();
    return;
  }
  
  console.log('Running LFAS Protocol integration examples...\n');
  
  // Uncomment to run examples:
  // await exampleBasicUsage();
  // await exampleFinancialVulnerability();
  // await exampleCrisisDetection();
  
  console.log('Examples complete! Uncomment the examples in main() to run them.');
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = {
  exampleBasicUsage,
  exampleFinancialVulnerability,
  exampleCrisisDetection
};
