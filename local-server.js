// Minimal dev proxy: OpenAI blocks direct browser CORS, so this forwards
// POST /api/openai-search to the Responses API and serves the static files.
// BYOK: each browser sends its own OpenAI key (from its localStorage) in the
// request body. This process never holds or stores a key of its own — it
// only relays the caller's key straight through to OpenAI, per request.
// Run: node local-server.js
// Open: http://127.0.0.1:8788 (prefer 127.0.0.1 — Cursor often binds ::1)
// Named local-server.js (not server.js) so Vercel does not treat this as the app entrypoint.
const http = require('http');
const fs = require('fs');
const path = require('path');
const net = require('net');

// 8788 avoids a common Cursor conflict on 8787 (EADDRINUSE / wrong process).
// Bind IPv4 loopback explicitly so "localhost" → ::1 does not hit another app.
const HOST = process.env.HOST || '127.0.0.1';
const PREFERRED_PORT = Number(process.env.PORT) || 8788;
const API_PATH = '/api/openai-search';

const MIME = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.mjs': 'text/javascript',
  '.css': 'text/css',
  '.pdf': 'application/pdf',
};

function normalizePath(url){
  const raw = (url || '/').split('?')[0];
  if(raw.length > 1 && raw.endsWith('/')) return raw.slice(0, -1);
  return raw;
}

function json(res, status, body, extraHeaders){
  res.writeHead(status, {
    'Content-Type': 'application/json',
    ...(extraHeaders || {})
  });
  res.end(JSON.stringify(body));
}

function createAppServer(){
  return http.createServer(async (req, res) => {
    const pathname = normalizePath(req.url);

    if(pathname === API_PATH){
      if(req.method !== 'POST'){
        json(res, 405, {
          error: 'Method Not Allowed — OpenAI proxy only accepts POST /api/openai-search. If you see this from GitHub Pages or another static host, use the Vercel app or run node local-server.js and open the printed URL.'
        }, { Allow: 'POST' });
        return;
      }

      let body = '';
      req.on('data', chunk => body += chunk);
      req.on('end', async () => {
        try{
          const { prompt, apiKey } = JSON.parse(body || '{}');
          if(!apiKey){
            json(res, 400, { error: 'missing OpenAI API key — add it in the page and save' });
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
          json(res, 500, { error: err.message });
        }
      });
      return;
    }

    // static file serving (GET/HEAD only — avoid confusing POSTs with HTML)
    if(req.method !== 'GET' && req.method !== 'HEAD'){
      json(res, 405, {
        error: `Method Not Allowed — static files are GET-only. OpenAI search must POST ${API_PATH} on this Node proxy (not GitHub Pages / Live Preview).`
      }, { Allow: 'GET, HEAD' });
      return;
    }

    let filePath = pathname === '/' ? '/index.html' : pathname;
    filePath = path.join(__dirname, decodeURIComponent(filePath));
    fs.readFile(filePath, (err, data) => {
      if(err){
        res.writeHead(404);
        res.end('not found');
        return;
      }
      const ext = path.extname(filePath);
      res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
      if(req.method === 'HEAD') res.end();
      else res.end(data);
    });
  });
}

function portFree(port, host){
  return new Promise((resolve) => {
    const tester = net.createServer()
      .once('error', () => resolve(false))
      .once('listening', () => tester.close(() => resolve(true)))
      .listen(port, host);
  });
}

async function pickPort(preferred, host){
  for(let p = preferred; p < preferred + 20; p++){
    if(await portFree(p, host)) return p;
  }
  throw new Error(`no free port near ${preferred} on ${host}`);
}

async function main(){
  const port = await pickPort(PREFERRED_PORT, HOST);
  const server = createAppServer();
  server.listen(port, HOST, () => {
    const url = `http://${HOST}:${port}`;
    console.log(`voice-job-radar dev server: ${url}`);
    console.log('OpenAI proxy: BYOK — relays each request\'s own key, holds none itself');
    if(port !== PREFERRED_PORT){
      console.log(`note: ${PREFERRED_PORT} was busy — using ${port} instead`);
    }
    console.log('Open this exact URL in the browser (prefer 127.0.0.1 over localhost).');
  });
  server.on('error', (err) => {
    console.error(err);
    process.exit(1);
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
