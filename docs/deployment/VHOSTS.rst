Apache + mod-wsgi configuration
===============================

An example Apache2 vhost configuration follows::

    WSGIDaemonProcess nederlandse_spoorwegen-<target> threads=5 maximum-requests=1000 user=<user> group=staff
    WSGIRestrictStdout Off

    <VirtualHost *:80>
        ServerName my.domain.name

        ErrorLog "/srv/sites/nederlandse_spoorwegen/log/apache2/error.log"
        CustomLog "/srv/sites/nederlandse_spoorwegen/log/apache2/access.log" common

        WSGIProcessGroup nederlandse_spoorwegen-<target>

        Alias /media "/srv/sites/nederlandse_spoorwegen/media/"
        Alias /static "/srv/sites/nederlandse_spoorwegen/static/"

        WSGIScriptAlias / "/srv/sites/nederlandse_spoorwegen/src/nederlandse_spoorwegen/wsgi/wsgi_<target>.py"
    </VirtualHost>


Nginx + uwsgi + supervisor configuration
========================================

Supervisor/uwsgi:
-----------------

.. code::

    [program:uwsgi-nederlandse_spoorwegen-<target>]
    user = <user>
    command = /srv/sites/nederlandse_spoorwegen/env/bin/uwsgi --socket 127.0.0.1:8001 --wsgi-file /srv/sites/nederlandse_spoorwegen/src/nederlandse_spoorwegen/wsgi/wsgi_<target>.py
    home = /srv/sites/nederlandse_spoorwegen/env
    master = true
    processes = 8
    harakiri = 600
    autostart = true
    autorestart = true
    stderr_logfile = /srv/sites/nederlandse_spoorwegen/log/uwsgi_err.log
    stdout_logfile = /srv/sites/nederlandse_spoorwegen/log/uwsgi_out.log
    stopsignal = QUIT

Nginx
-----

.. code::

    upstream django_nederlandse_spoorwegen_<target> {
      ip_hash;
      server 127.0.0.1:8001;
    }

    server {
      listen :80;
      server_name  my.domain.name;

      access_log /srv/sites/nederlandse_spoorwegen/log/nginx-access.log;
      error_log /srv/sites/nederlandse_spoorwegen/log/nginx-error.log;

      location /500.html {
        root /srv/sites/nederlandse_spoorwegen/src/nederlandse_spoorwegen/templates/;
      }
      error_page 500 502 503 504 /500.html;

      location /static/ {
        alias /srv/sites/nederlandse_spoorwegen/static/;
        expires 30d;
      }

      location /media/ {
        alias /srv/sites/nederlandse_spoorwegen/media/;
        expires 30d;
      }

      location / {
        uwsgi_pass django_nederlandse_spoorwegen_<target>;
      }
    }
