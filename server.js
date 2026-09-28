/**
 * TerraSeek — Local Development Server
 * Simple HTTP server for the prototype frontend.
 * Run: node server.js
 * Then open: http://localhost:3000
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = Number(process.env.PORT || 3000);
const FRONTEND_DIR = path.join(__dirname, 'frontend');
const DATA_DIR = path.join(__dirname, 'data');

const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css':  'text/css; charset=utf-8',
    // text/javascript is the most broadly compatible MIME type for the
    // prototype's in-app browser and avoids strict MIME execution failures.
    '.js':   'text/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png':  'image/png',
    '.jpg':  'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.svg':  'image/svg+xml',
    '.ico':  'image/x-icon',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
};

const server = http.createServer((req, res) => {
    let url = req.url.split('?')[0]; // strip query string

    // Default to index.html
    if (url === '/' || url === '') {
        url = '/index.html';
    }

    const rootDir = url.startsWith('/data/') ? DATA_DIR : FRONTEND_DIR;
    const relativeUrl = url.startsWith('/data/') ? url.slice('/data'.length) : url;
    const filePath = path.resolve(rootDir, `.${relativeUrl}`);

    // Security: prevent directory traversal
    if (!filePath.startsWith(path.resolve(rootDir) + path.sep)) {
        res.writeHead(403);
        res.end('Forbidden');
        return;
    }

    fs.readFile(filePath, (err, data) => {
        if (err) {
            if (err.code === 'ENOENT') {
                // SPA fallback: serve index.html for unknown routes
                fs.readFile(path.join(FRONTEND_DIR, 'index.html'), (err2, indexData) => {
                    if (err2) {
                        res.writeHead(500);
                        res.end('Internal Server Error');
                        return;
                    }
                    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                    res.end(indexData);
                });
            } else {
                res.writeHead(500);
                res.end('Internal Server Error');
            }
            return;
        }

        const ext = path.extname(filePath).toLowerCase();
        const contentType = MIME_TYPES[ext] || 'application/octet-stream';

        res.writeHead(200, {
            'Content-Type': contentType,
            'Cache-Control': 'no-cache',
        });
        res.end(data);
    });
});

server.listen(PORT, () => {
    console.log(`
  ┌──────────────────────────────────────────────┐
  │                                              │
  │   ◈ TERRASEEK  Evidence Engine               │
  │   Prototype server running                   │
  │                                              │
  │   Local:  http://localhost:${PORT}              │
  │                                              │
  │   Press Ctrl+C to stop                       │
  │                                              │
  └──────────────────────────────────────────────┘
    `);
});
