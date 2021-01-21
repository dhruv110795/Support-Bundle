# SupportBundle
Support bundle for Karthavya Projects

CONFIGURE MONGO Details in config.py

cd install
sudo sh install_dependencies.sh

http://localhost:9090 Opens Support bundle web.

API's:

1) Reload config--->
    URL         : http://localhost:9090/reload_config
    METHOD      : GET 
    DESCRIPTION : Reloads the Support Bundle config without restarting the service.

2) Get Config--->
    URL         : http://localhost:9090/config
    METHOD      : GET 
    DESCRIPTION : Provides information about enabled projects for Support Bundle.
  
3) Download Support Bundle--->
    URL         : http://localhost:9090/support_bundle?project=PROJECTNAME&mongo_dump=true&app_log_dump=true&title=BUNDLETILE&bundle_type=zip&sys_log_dump=true
    METHOD      : GET 
    DESCRIPTION : Provides information about enabled projects for Support Bundle.

4) Get Recent Dumps-->
    URL         : http://localhost:9090/recent_dumps
    METHOD      : GET 
    DESCRIPTION : Provides information about recent Support Bundle Dumps.

5) Download Old Support Bundle--->
    URL         : http://localhost:9090/download/SUPPORT_BUNDLE_PATH
    METHOD      : GET 
    DESCRIPTION : Downloads old support bundle.


6) Delete Support Bundle--->
    URL         : http://localhost:9090/support_bundle/SUPPORT_BUNDLE_PATH
    METHOD      : DELETE 
    DESCRIPTION : Deletes Support Bundle Dumps.
