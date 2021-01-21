import os
import json
import uuid
import string
import socket
import random
import bottle
import tarfile
import zipfile
import datetime
import importlib

import utils
import config as conf

logger = utils.get_logger(conf.LOG_PATH)

def bottle_abort(status, error_msg):

    if type(error_msg) not in [str]:
        error_msg = json.dumps(error_msg)

    raise bottle.HTTPResponse(
                body=error_msg,
                status=status,
                headers={'Content-type': 'application/json'}
            )

def random_string(length):
    return "".join([random.choice(string.ascii_letters +
                                  string.digits) for i in range(length)])

def add_users():
    status = {}

    try:
        users = {"users":[{'_id':'1', 'username':'admin', 'password':'k@rth@vy@', "access_token":str(uuid.uuid4())},{'_id':'2', 'username':'support', 'password':'bundle', "access_token":str(uuid.uuid4())}]}
        if not os.path.exists(conf.USERS_JSON_PATH):
            with open(conf.USERS_JSON_PATH, "w") as f:
                f.write(json.dumps(users))
            
            logger.info("Default users created.")
    except Exception as ex:
        status["error"] = str(ex)
        return status


def check_authorized():
    session_id = None
    access_token = bottle.request.get_header("access_token") if bottle.request.get_header("access_token") else None
    errors = []
    if access_token is None:
        session_id = bottle.request.get_cookie('session_id', None)

    try:
        
        if not os.path.exists(conf.USERS_JSON_PATH):
            add_users()
        
        with open(conf.USERS_JSON_PATH) as f:
            users = json.loads(f.read())

        if session_id:
            for user in users["users"]:
                if session_id == user.get("session_id"):
                    return user

            errors.append('errors.unauthorized')
        
        elif access_token:
            for user in users["users"]:
                if access_token == user["access_token"]:
                    return user
            errors.append('errors.unauthorized')
        else:
            errors.append('errors.unauthorized')
    except Exception as ex:
        errors.append(str(ex))
    if errors:
        bottle_abort(401, json.dumps({'errors': errors}))


@bottle.route("/sessions", method='POST')
@bottle.route("/sessions/", method='POST')
def create_session():
    errors = []
    username = None
    password = None
    success = False
    db_user = None
    form = None
    session_id = None
    status = {}
    try:        
        form = json.loads(bottle.request.body.read().decode("utf-8"))
        username = form.get('username', '')
        password = form.get('password', '')

        if not username or not password :
            errors.append('empty.username or empty.password')
    except Exception as ex1:
        status["create_session Exception"] = str(ex1)
        errors.append('error.parse')
    if errors:
        logger.error( "create_session : error : %s" %str(errors) )
        bottle_abort(401, json.dumps({ 'errors' : errors}))
    try:
        if not os.path.exists(conf.USERS_JSON_PATH):
            add_users()
        
        with open(conf.USERS_JSON_PATH) as f:
            users = json.loads(f.read())
          
        db_user = {}
        for user in users["users"]:
            if username == user["username"] and password == user["password"]:
                db_user = user

        if db_user:

            if db_user.get("session_id", None) is not None:
                # msg = {"msg_type":"relogin","data":db_user}
                # utils.send_to_notifier(msg)
                pass

            session_id = random_string(16)
            db_user["session_id"] = session_id
            db_user["logged_in"] = True

            with open(conf.USERS_JSON_PATH, "w") as f:
                f.write(json.dumps(users))
            
            bottle.response.set_cookie('session_id', session_id)
            
            db_user["_id"] = str(db_user["_id"])
            return db_user
        else:
            raise Exception ('Not a valid user')

    except Exception as ex:
        logger.error("create_session: Exception: %s" %str(ex))
        bottle_abort(500, json.dumps({ 'errors' : [str(ex)]}))

@bottle.route("/sessions" ,method="DELETE")
@bottle.route("/sessions/<session_id>" ,method="DELETE")
def sign_out(session_id=None):
    session_user = None
    session_user = check_authorized()
    try:
        if session_user:
            username = session_user["username"]
            
                    
            with open(conf.USERS_JSON_PATH) as f:
                users = json.loads(f.read())
            
            db_user = {}
            for user in users["users"]:
                if username == user["username"]:
                    db_user = user

            if db_user:
                if "session_id" in db_user:
                    del db_user["session_id"]

                if "logged_in" in db_user:
                    del db_user["logged_in"]

                with open(conf.USERS_JSON_PATH, "w") as f:
                    f.write(json.dumps(users))            

        return {"user" :"%s successfully logged out"%str(user)}
    except Exception as e:
        logger.error("exception occured %s"%str(e))
        bottle_abort(500,json.dumps({"errors":str(e)}))


@bottle.route("/download/<path:path>")
def serve_dump_file(path):
    check_authorized()
    if not path.startswith("/"):
        path = "/" + path
    if not path.startswith(conf.DUMP_FOLDER_PATH):
        return 
    return bottle.static_file(os.path.basename(path), root=os.path.dirname(path))


@bottle.route("/support_bundle/<path:path>", method="DELETE")
def service_dump_file(path):
    check_authorized()
    if not path.startswith("/"):
        path = "/" + path
    if not path.startswith(conf.DUMP_FOLDER_PATH):
        return 
    
    if os.path.exists(path):
        os.remove(path)   
    return 


@bottle.route("/recent_dumps")
def get_recent_dumps():
    check_authorized()
    resp = {"dumps":[]}
    for file_ in os.listdir(conf.DUMP_FOLDER_PATH):
        if file_.endswith(".zip") or file_.endswith(".tar.gz") or  file_.endswith(".tar.bz2"):
            project_name = "Unknown"
            for val in os.path.basename(file_).split("_"):
                try:
                    conf.PROJECT_CONFIGURATION[val]
                    project_name = val
                    break
                except KeyError:
                    pass
            try:
                time = os.path.splitext(os.path.basename(file_))[0].split("__")[-1].replace("_",":")
            except:
                time = "00:00:00"

            time = time.split(".")[0] 
            try:
                day = os.path.splitext(os.path.basename(file_))[0].split("__")[0].split("_")[-1]
            except:
                day = datetime.datetime.now().strftime("%d-%m-%Y")

            resp["dumps"].append({"day":day,"time":time,"project":project_name,"file_name":os.path.basename(file_), "path": os.path.join(conf.DUMP_FOLDER_PATH, file_)})
    return resp
    

@bottle.route("/config")
def get_config():
    check_authorized()
    resp = {"config":{"enabled_projects":[], "client_name":conf.CLIENT_NAME}}
    for project, config in conf.PROJECT_CONFIGURATION.items():
        if config["PROJECT_ENABLED"]:
            resp["config"]["enabled_projects"].append(project)
    return resp


@bottle.route("/support_bundle")
def get_support_bundle():
    check_authorized()
    project = bottle.request.query.project if bottle.request.query.project else None
    bundle_type = bottle.request.query.bundle_type if bottle.request.query.bundle_type else "zip"

    if bundle_type.lower() not in ["zip", "tar.gz", "tar.bz2"]:
        bundle_type = "zip"
    
    if project is None:
        bottle_abort(500, {"error":"Project Name is not provided"}) 

    project_conf = conf.PROJECT_CONFIGURATION.get(project, None)
    if project_conf is None:
        bottle_abort(500, {"error":"Project {} is not yet supported".format(project)})
    
    if not project_conf["PROJECT_ENABLED"]:
        bottle_abort(500, {"error":"Project {} is not Enabled".format(project)})
    
    zip_file_name = "{}_{}".format(conf.CLIENT_NAME, project)
    if bottle.request.query.title:
        zip_file_name = "{}_{}".format(bottle.request.query.title, zip_file_name)
    
    take_mongo_dump = False
    if bottle.request.query.mongo_dump:
        take_mongo_dump = True
        zip_file_name = "{}_{}".format(zip_file_name, "mongo_dump")
    
    take_log_dump = False 
    if bottle.request.query.app_log_dump:
        take_log_dump = True 
        zip_file_name = "{}_{}".format(zip_file_name, "app_logs")

    take_sys_log_dump = False 
    if bottle.request.query.sys_log_dump:
        take_sys_log_dump = True 
        zip_file_name = "{}_{}".format(zip_file_name, "sys_logs")

    zip_file_path = os.path.join(conf.DUMP_FOLDER_PATH, "{}_{}_{}.{}".format(zip_file_name, utils.get_host_name(),datetime.datetime.now().strftime("%d-%m-%Y__%H_%M_%S"), bundle_type))
    logger.info("[get_support_bundle][Webservice][ZIP_FILE:({}), MONGO_DUMP:({}), LOG_DUMP:({})]".format(zip_file_name, take_mongo_dump, take_log_dump))
    try:
        if take_log_dump or take_mongo_dump:
  
            if bundle_type == "zip":

                if project_conf.get("ENABLE_PASSWORD_ZIP", False):
                    password = project_conf.get("LOG_DUMP_PASSWORD") if take_log_dump else project_conf.get("DB_DUMP_PASSWORD")
                    utils.pyminizip_compressor(zip_file_path, project_conf, take_log_dump, take_mongo_dump, take_sys_log_dump, password)
                else:
                    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_f:    
                       utils.zipfile_compressor(zip_f, project_conf, zip_f.write, take_log_dump, take_mongo_dump, take_sys_log_dump)

            elif "tar" in bundle_type:
                if bundle_type == "tar.gz":
                    mode = "w:gz"
                else:
                    mode = "w:bz2"
                with tarfile.open(zip_file_path, mode, compresslevel=1) as tar:
                    utils.zipfile_compressor(tar, project_conf, tar.add, take_log_dump, take_mongo_dump, take_sys_log_dump)

            resp = bottle.static_file(os.path.basename(zip_file_path), root=conf.DUMP_FOLDER_PATH, download=True)
            resp.set_header("Set-Cookie", "fileDownload=true; path=/")
            return resp
    
    except Exception as e:
        logger.error("[get_support_bundle][Webservice][Exception->{}]".format(e))
        bottle_abort(500, {"errors":str(e)})

@bottle.route('/reload_config')
def reload_config():
    check_authorized()
    importlib.reload(conf)

@bottle.route('/web/<path:path>')
def serve_static_file(path):
    try:
        return bottle.static_file(path, root=conf.WEB_FOLDER_PATH)
    except Exception as ex:
        logger.error("[serve_static_file][webservice]:[Exception {}]".format(ex))


@bottle.route('/')
def redirect_to_default_page():
    return bottle.redirect("/web/index.html")


if __name__ == "__main__":
    if not os.path.exists(conf.DUMP_FOLDER_PATH):
        os.makedirs(conf.DUMP_FOLDER_PATH)

    add_users()
    
    bottle.run(host="0.0.0.0", port=9090, server="twisted", debug=True)
