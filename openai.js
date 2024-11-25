const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');

// Azure OpenAI settings
const OPENAI_API_KEY = 'YOUR_AZURE_OPENAI_API_KEY';
const OPENAI_ENDPOINT = 'https://YOUR_AZURE_OPENAI_ENDPOINT/openai/deployments/YOUR_DEPLOYMENT_NAME/completions?api-version=2023-03-15-preview';

// Telegram Bot Token
const TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN';

// Initialize the Telegram bot
const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: true });

// Function to chat with Azure OpenAI
async function chatWithOpenAI(prompt) {
    try {
        const response = await axios.post(
            OPENAI_ENDPOINT,
            {
                prompt: prompt,
                max_tokens: 150,
                temperature: 0.7,
            },
            {
                headers: {
                    'Authorization': `Bearer ${OPENAI_API_KEY}`,
                    'Content-Type': 'application/json',
                },
            }
        );
        return response.data.choices[0].text.trim();
    } catch (error) {
        console.error('Error with OpenAI:', error.message);
        return "Sorry, I couldn't connect to OpenAI.";
    }
}

// Handle start command
bot.onText(/\/start/, (msg) => {
    bot.sendMessage(msg.chat.id, "Hello! I'm your AI bot. Ask me anything!");
});

// Handle user messages
bot.on('message', async (msg) => {
    if (msg.text.startsWith('/')) return; // Ignore commands
    const response = await chatWithOpenAI(msg.text);
    bot.sendMessage(msg.chat.id, response);
});
