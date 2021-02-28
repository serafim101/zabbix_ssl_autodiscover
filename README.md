# Zabbix SSL certificates check
Zabbix SSL certificates check with autodiscovering vhosts on Nginx web-server

This template allows you to monitor the ssl certificate expiration date on the side of your web server. This modification differs from others in that it allows you to assign a template to a web server and, using autodiscovery, recognize existing virtual hosts on the side of your web server and automatically create the necessary items and triggers.
This template is suitable exclusively for nginx web server, apache is not supported yet.

For the script to work, you need to install the python libraries
* json
* pyparsing
* string

How does he work? Using a python script, information about your virtual hosts is collected, which are located in the nginx settings. To do this, you need to pass to the parser.py script the location of the directory where the configuration files with the settings of your nginx virtual hosts are located (passed using a macro in the {$ CONF_LOCATION} template settings). Then a bash script is launched which, using the standard openssl utility, finds out the necessary information about the certificate

This template is based on 2 scripts:
* Nginx Configuration Parser - https://github.com/fatiherikli/nginxparser
* https-ssl-cert-check-zabbix - https://github.com/selivan/https-ssl-cert-check-zabbix

In the case of the Nginx Configuration Parser, I integrated its functionality into the parser.py script, but we still MUST thank the author for such an amazing nginx configuration parser (https://github.com/fatiherikli/nginxparser).
I integrated the Nginx Configuration Parser functions inside my script solely for convenience! I do not claim the copyright of the owner and I openly declare this!

##Installation and use.

The scripts must be installed in the directory with custom parameters zabbix_agentd (by default /etc/zabbix/zabbix_agentd.d/). If your path to the settings of user parameters is different from the standard, then you will need to specify the correct location of all scripts in the file userparameter_ssl.conf.

####Macros:
* {$ CHECK_TIMEOUT} - timeout for waiting for a response from the server when requesting script information
* {$ CONF_LOCATION} - location with virtual host settings for your nginx web server. IMPORTANT! At the end, specify the '/' sign, otherwise the script will not work. Invalid argument: / etc / nginx / sites-available, valid argument: / etc / nginx / sites-available /
* {$ SSL_HOST} - the host to which requests will be made. By default, this is localhost
* {$ SSL_PORT} - port on which HTTPS is running, by default 443

This template was tested on Debian 10 Buster and Zabbix 5.2.
