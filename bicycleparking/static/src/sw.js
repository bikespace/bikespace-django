
var dataCacheName = 'bikespace-v1';
var cacheName = 'bikespace';
var filesToCache = [
  'https://s3.amazonaws.com/bikespace-static/dist/bundle.js',
  'https://s3.amazonaws.com/bikespace-static/dist/style/stylesheet.css',
  'https://s3.amazonaws.com/bikespace-static/dist/style/mobilesheet.css',
  'https://s3.amazonaws.com/bikespace-static/dist/style/flatpickr.min.css',
  'https://s3.amazonaws.com/bikespace-static/dist/style/leaflet.css',
  'https://s3.amazonaws.com/bikespace-static/dist/style/leaflet-search.css',
  '/'
];

self.addEventListener('install', function(e) {
  console.log('[ServiceWorker] Install');
  e.waitUntil(
    caches.open(cacheName).then(function(cache) {
      console.log('[ServiceWorker] Caching app shell');
      return cache.addAll(filesToCache);
    })
  );
});

self.addEventListener('activate', function(e) {
  console.log('[ServiceWorker] Activate');
  e.waitUntil(
    caches.keys().then(function(keyList) {
      return Promise.all(keyList.map(function(key) {
        if (key !== cacheName && key !== dataCacheName) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  return self.clients.claim();
});

