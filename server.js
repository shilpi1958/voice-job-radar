// Minimal dev proxy: OpenAI blocks direct browser CORS, so this forwards
// POST /api/openai-search to the Responses API and serves the static files.
// BYOK: each browser sends its own OpenAI key (from its localStorage) in the
// request body. This process never holds or stores a key of its own — it
// only relays the caller's key straight through to OpenAI, per request.
// Run: node server.js
const http = require('http');
const fs = require('fs');
const path = require('path');

// 8788 avoids a common Cursor conflict on 8787 (EADDRINUSE / wrong process).
const PORT = process.env.PORT || 8788;

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };

const server = http.createServer(async (req, res) => {
  if(req.method === 'POST' && req.url === '/api/openai-search'){
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', async () => {
      try{
        const { prompt, apiKey } = JSON.parse(body);
        if(!apiKey){
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'missing OpenAI API key — add it in the page and save' }));
          return;
        }
        const upstream = await fetch('https://api.openai.com/v1/responses', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
          },
          body: JSON.stringify({
            model: 'gpt-5.6',
            tools: [{ type: 'web_search' }],
            input: prompt
          })
        });
        const data = await upstream.json();
        res.writeHead(upstream.status, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(data));
      }catch(err){
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }

  // static file serving
  let filePath = req.url === '/' ? '/index.html' : req.url;
  filePath = path.join(__dirname, decodeURIComponent(filePath.split('?')[0]));
  fs.readFile(filePath, (err, data) => {
    if(err){
      res.writeHead(404);
      res.end('not found');
      return;
    }
    const ext = path.extname(filePath);
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log(`voice-job-radar dev server: http://localhost:${PORT}`);
  console.log('OpenAI proxy: BYOK — relays each request\'s own key, holds none itself');
});
