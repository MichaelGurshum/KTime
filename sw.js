// sw.js - Service Worker

self.addEventListener('install', (event) => {
  console.log('Service Worker installed');
  self.skipWaiting(); // activate immediately
});

self.addEventListener('activate', (event) => {
  console.log('Service Worker activated');
});

// Listen for push events (if you add a push server later)
self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};
  const title = data.title || "שם לפי שעה";
  const options = {
    body: data.body || "שם לפי שעה - שעה חדשה",
    icon: data.icon || "/icon.png",
    badge: data.badge || "/icon.png"
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

// Optional: handle notification click
self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  event.waitUntil(clients.openWindow('/')); // open homepage
});
