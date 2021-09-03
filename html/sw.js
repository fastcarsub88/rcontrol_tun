var cacheName = 'rcontrol_tun-v2';
var filesToCache = [
  "index.js?"+cacheName,
  "style.css?"+cacheName,
  "manifest.json?"+cacheName,
  "index.html?"+cacheName,
  "img/maskicon.png?"+cacheName
]
self.addEventListener('install', function(e) {
  console.log('installing sw '+cacheName);
  self.skipWaiting();
  e.waitUntil(
    caches.open(cacheName).then(function(cache) {
      cache.addAll(filesToCache);
    })
  );
});

self.addEventListener('activate',  event => {
  event.waitUntil(
    caches.keys().then(keys=> Promise.all(
      keys.map(key=>{
        if (cacheName != key) {
          return caches.delete(key);
        }
      })
    )).then(()=>{
      console.log(cacheName+' is activated');
    })
  );
});

self.addEventListener(
  'fetch',
  event => {
    var a = event.request.url;
    var b = a.substr(a.lastIndexOf('/'));
    if (b == '/api') { return };
    if (b == '/') {
      event.respondWith(caches.match('index.html'))
      return
    }
    event.respondWith(caches.match(event.request);
  }
)
