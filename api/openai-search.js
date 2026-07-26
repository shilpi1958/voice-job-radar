// Vercel serverless OpenAI proxy — mirrors local-server.js BYOK relay.
// Browser sends { prompt, apiKey }; we forward to Responses API and never store the key.
// CORS allows GitHub Pages (or any origin) to call this when the app is not same-origin.

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Vary', 'Origin');

  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST, OPTIONS');
    res.status(405).json({
      error:
        'Method Not Allowed — OpenAI proxy only accepts POST /api/openai-search.',
    });
    return;
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};
    const { prompt, apiKey } = body;
    if (!apiKey) {
      res.status(400).json({
        error: 'missing OpenAI API key — add it in the page and save',
      });
      return;
    }

    const upstream = await fetch('https://api.openai.com/v1/responses', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: 'gpt-5.6',
        tools: [{ type: 'web_search' }],
        input: prompt,
      }),
    });

    const data = await upstream.json();
    res.status(upstream.status).json(data);
  } catch (err) {
    res.status(500).json({ error: err.message || String(err) });
  }
};
