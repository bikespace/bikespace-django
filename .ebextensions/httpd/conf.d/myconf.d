RewriteEngine On
RewriteCond %{HTTP:X-Forwarded-Proto} =http
RewriteRule . https://%{HTTP:Host}%{REQUEST_URI} [L,R=permanent]