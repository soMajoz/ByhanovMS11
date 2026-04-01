const CACHE_NAME = 'news-v1';
const ASSETS = [ '/', '/index.html', '/src/css/style.css', '/src/js/app.js', '/src/js/db.js', '/manifest.json' ];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))); });
self.addEventListener('fetch', e => { e.respondWith(caches.match(e.request).then(res => res || fetch(e.request))); });
