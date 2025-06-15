require('dotenv').config();
const { Telegraf } = require('telegraf');
const axios = require('axios');

const bot = new Telegraf(process.env.BOT_TOKEN);
const openaiApiKey = process.env.OPENAI_API_KEY;

bot.start((ctx) => {
  ctx.reply('Привет, это AI managed 🤖\n\nНапиши:\n\nНиша: ...\nЦА: ...\nПредложение: ...\n\nЯ сгенерирую 2 оффера.');
});

bot.on('text', async (ctx) => {
  const input = ctx.message.text;

  const prompt = `
Ты — AI-ассистент для создания продающих офферов.
Сгенерируй 2 оффера по шаблону:

🎯 Оффер для ниши: [указать]
1. 💡 Что предлагаешь
2. 🔥 Почему это важно
3. 🧠 Кто ты
4. 🚀 Призыв к действию

+ Варианты заголовков и CTA

Вводные:
${input}
`;

  try {
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-4o',
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.7
      },
      {
        headers: {
          'Authorization': `Bearer ${openaiApiKey}`,
          'Content-Type': 'application/json'
        }
      }
    );

    const result = response.data.choices[0].message.content;
    ctx.reply(result);
  } catch (error) {
    console.error(error.response?.data || error.message);
    ctx.reply('⚠️ Ошибка. Проверь OpenAI ключ.');
  }
});

bot.launch();
console.log('🤖 AI managed bot запущен');
