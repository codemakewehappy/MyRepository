 #!/bin/bash
    cd /home/code/Repository

    kill -9 $(pidof uwsgi)
     /usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
     /usr/local/nginx/sbin/nginx -s reload 
    /usr/bin/uwsgi --ini uwsgi.ini 
 