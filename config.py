import os

#######################################CONSTANTS##########################################################
CLIENT_NAME                            = "Karthavya-229"

MAM_PROJECT_NAME                       = "MAM"
HSM_PROJECT_NAME                       = "HSM"
HYPE_PROJECT_NAME                      = "HYPE"
MAM3_PROJECT_NAME                      = "MAM3"
TRANSCODER_PROJECT_NAME                = "TRANSCODER"

MONGO_DEPLOYMENT_STANDALONE            = 1
MONGO_DEPLOYMENT_REPLICA_SET           = 2

PROTOCOL_FTP                           = "FTP"
PROTOCOL_SMB                           = "SMB"

SCHEDULE_INTERVAL_HOURLY               = "Hourly"
SCHEDULE_INTERVAL_DAILY                = "Daily"
SCHEDULE_INTERVAL_WEEKLY               = "Weekly"

SUPPORT_BUNDLE_PATH                    = os.path.dirname(os.path.abspath(__file__))
DUMP_FOLDER_PATH                       = os.path.join(SUPPORT_BUNDLE_PATH, "tmp")
WEB_FOLDER_PATH                        = os.path.join(SUPPORT_BUNDLE_PATH, "web")
LOG_PATH                               = os.path.join(SUPPORT_BUNDLE_PATH, "logs", "SupportBundle.log")
JSON_CRON_CONFIGURATION_PATH           = os.path.join(SUPPORT_BUNDLE_PATH, "config.json")
USERS_JSON_PATH                        = os.path.join(SUPPORT_BUNDLE_PATH, "users.json")

if os.name == "posix":
    MONGODUMP_BINARY_FILE              = "/usr/bin/mongodump"
else:
    MONGODUMP_BINARY_FILE              = "C:\\Program Files\\MongoDB\\Server\\4.0\\bin\\mongodump.exe"#C:\\Program Files\\MongoDB 2.6 Standard Legacy\\bin\\mongodump.exe

#########################################################################################################
BACKUP_BUNDLE_TO_REMOTE_STORAGE        = False
BACKUP_STORAGE_PROTOCOL_TO_USE         = PROTOCOL_FTP #PROTOCOL_FTP/PROTOCOL_SMB
MAX_BACKUP_BUNDLES_TO_KEEP_PER_PROJECT = 3
 
BACKUP_STORAGE_INFO                    = {
                                          PROTOCOL_FTP : { "FTP_IP"        :  "127.0.0.1",
                                                           "FTP_PORT"      :  "21",
                                                           "OFFSET_PATH"   :  "/",
                                                           "USERNAME"      :  "ftp_username",
                                                           "PASSWORD"      :  "ftp_password"
                                                         },
                                          PROTOCOL_SMB : { "SMB_IP"        : "127.0.0.1",
                                                           "SMB_SHARENAME" : "share_name",
                                                           "SMB_USERNAME"  : "smb_username",
                                                           "SMB_PASSWORD"  : "smb_password"
                                                         }
                                         }
#####################################PROJECTS CONFIGURATION##############################################
PROJECT_CONFIGURATION = {
        
        HYPE_PROJECT_NAME : { 
                            "PROJECT_ENABLED"       : False,
                            "MONGO_DB_IP"           : "127.0.0.1",
                            "MONGO_DB_PORT"         : "27017",
                            "MONGO_DEPLOYMENT_TYPE" : MONGO_DEPLOYMENT_STANDALONE,
                            "DB_AUTHENTICATION"     : False,
                            "DB_USERNAME"           : "socialmedia",
                            "DB_PASSWORD"           : "socialmedia",
                            "DB_NAME"               : "socialmedia",
                            "SUPERVISOR_LOG_PATH"   : "/opt/logs/supervisor",
                            "SUPERVISOR_LOG_FILES"  : ("SocialMedia_BroadcastManager","SocialMedia_Handler",\
                                                       "SocialMedia_LoginServiceHandler", "SocialMedia_Notifier",
                                                       "SocialMedia_Webservice"),
                            "LOG_PATH"              : "/opt/logs/social_media",
                            "LOG_FILES"             : ("social_media.log",),
                            "ENABLE_PASSWORD_ZIP"   : True,
                            "LOG_DUMP_PASSWORD"     : "k@rth@vy@",
                            "DB_DUMP_PASSWORD"      : "@dm1nKTPL",
                            "SCHEDULE"              : { "SCHEDULE_ENABLED"       : True,
                                                        "SCHEDULE_INTERVAL"      : SCHEDULE_INTERVAL_DAILY, 
                                                        "SCHEDULE_TIME"          : "00:00:00"}#HH:MM:SS
                        },
        
        TRANSCODER_PROJECT_NAME : { 
                            "PROJECT_ENABLED"       : False,
                            "MONGO_DB_IP"           : "127.0.0.1", #()
                            "MONGO_DB_PORT"         : "27017",
                            "MONGO_DEPLOYMENT_TYPE" : MONGO_DEPLOYMENT_STANDALONE,
                            "DB_AUTHENTICATION"     : False,
                            "DB_USERNAME"           : "transcoder",
                            "DB_PASSWORD"           : "transcoder",
                            "DB_NAME"               : "transcoder",
                            "SUPERVISOR_LOG_PATH"   : "/opt/logs/supervisor",
                            "SUPERVISOR_LOG_FILES"  : ("Transcoder_Binstatus","Transcoder_Mediapoller",\
                                                       "Transcoder_Notifier", "Transcoder_JobsHandler",
                                                       "Transcoder_WebService"),
                            "LOG_PATH"              : "/opt/Transcoder/logs", #C:\\Karthavya\\logss
                            "LOG_FILES"             : ("transcoder_binstatus.log", "transcoder_jobshandler.log", "transcoder_notifier.log",
                                                       "transcoder_poller.log", "transcoder_webservice.log"),
                            "ENABLE_PASSWORD_ZIP"   : True,
                            "LOG_DUMP_PASSWORD"     : "k@rth@vy@",
                            "DB_DUMP_PASSWORD"      : "@dm1nKTPL",
                            
                            "SCHEDULE"              : { "SCHEDULE_ENABLED"       : True,
                                                        "SCHEDULE_INTERVAL"      : SCHEDULE_INTERVAL_DAILY, 
                                                        "SCHEDULE_TIME"          : "00:00:00"}#HH:MM:SS
                        },

        HSM_PROJECT_NAME : {  
                           "PROJECT_ENABLED"       : False,
                            "MONGO_DB_IP"           : "127.0.0.1", #()
                            "MONGO_DB_PORT"         : "27017",
                            "MONGO_DEPLOYMENT_TYPE" : MONGO_DEPLOYMENT_STANDALONE,
                            "DB_AUTHENTICATION"     : False,
                            "DB_USERNAME"           : "hsm",
                            "DB_PASSWORD"           : "adm1nKTPL20i9",
                            "DB_NAME"               : "hsm",
                            "SUPERVISOR_LOG_PATH"   : "/opt/logs/supervisor",
                            "SUPERVISOR_LOG_FILES"  : (),
                            "LOG_PATH"              : "C:\\Karthavya\\logs",
                            "LOG_FILES"             : ("webservice.log","cachedevice.log","diskdevice.log",\
                                                       "notifier.log","ltomanualdevice.log","ltolibrary.log",\
                                                       "odamanualdevice.log","odalibrary.log","cachecleanup.log",
                                                       "poller.log","workflow.log","dvd.log", "default.log",
                                                       "mam_archived_assets_migration_to_hsm.log", "service-configurator.log"),
                            "ENABLE_PASSWORD_ZIP"   : True,
                            "LOG_DUMP_PASSWORD"     : "k@rth@vy@",
                            "DB_DUMP_PASSWORD"      : "@dm1nKTPL",
                            
                            "SCHEDULE"              : { "SCHEDULE_ENABLED"       : True,
                                                        "SCHEDULE_INTERVAL"      : SCHEDULE_INTERVAL_DAILY, 
                                                        "SCHEDULE_TIME"          : "00:00:00"}#HH:MM:SS
                        },
        
        
        MAM3_PROJECT_NAME : { 
                            "PROJECT_ENABLED"       : False,
                            "MONGO_DB_IP"           : "127.0.0.1", #()
                            "MONGO_DB_PORT"         : "27017",
                            "MONGO_DEPLOYMENT_TYPE" : MONGO_DEPLOYMENT_STANDALONE,
                            "DB_AUTHENTICATION"     : False,
                            "DB_USERNAME"           : "mediaworker",
                            "DB_PASSWORD"           : "mediaworker",
                            "DB_NAME"               : "media_worker1x",
                            "SUPERVISOR_LOG_PATH"   : "/opt/logs/supervisor",
                            "SUPERVISOR_LOG_FILES"  : (),
                            "LOG_PATH"              : "/opt/logs/mw",
                            "LOG_FILES"             : ("mw_event_listener.log", "mw_generic.log", "mw_hsm.log",\
                                                       "mw_mediapoller.log", "mw_mediaworker.log", "mw_nodestats.log",
                                                      "mw_webservice.log"),
                            "ENABLE_PASSWORD_ZIP"   : True,
                            "LOG_DUMP_PASSWORD"     : "k@rth@vy@",
                            "DB_DUMP_PASSWORD"      : "@dm1nKTPL",
                            
                            "SCHEDULE"              : { "SCHEDULE_ENABLED"       : True,
                                                        "SCHEDULE_INTERVAL"      : SCHEDULE_INTERVAL_DAILY, 
                                                        "SCHEDULE_TIME"          : "00:00:00"}#HH:MM:SS
                        },

        MAM_PROJECT_NAME :  { 
                            "PROJECT_ENABLED"       : False,
                            "MONGO_DB_IP"           : "127.0.0.1", #()
                            "MONGO_DB_PORT"         : "27017",
                            "MONGO_DEPLOYMENT_TYPE" : MONGO_DEPLOYMENT_STANDALONE,
                            "DB_AUTHENTICATION"     : False,
                            "DB_USERNAME"           : "mediaworker",
                            "DB_PASSWORD"           : "mediaworker",
                            "DB_NAME"               : "media_worker1x",
                            "SUPERVISOR_LOG_PATH"   : "/opt/logs/supervisor",
                            "SUPERVISOR_LOG_FILES"  : ("MW_","Elast","Image"),
                            "LOG_PATH"              : "/opt/logs/mw",
                            "LOG_FILES"             : ("mw_event_listener.log", "mw_generic.log", "mw_hsm.log",\
                                                       "mw_mediapoller.log", "mw_mediaworker.log", "mw_nodestats.log",
                                                       "mw_webservice.log", "mw_emailAlertService.log","mw_image_process.log"),
                            "ENABLE_PASSWORD_ZIP"   : True,
                            "LOG_DUMP_PASSWORD"     : "k@rth@vy@",
                            "DB_DUMP_PASSWORD"      : "@dm1nKTPL",
                                                        
                            "SCHEDULE"              : { "SCHEDULE_ENABLED"       : True,
                                                        "SCHEDULE_INTERVAL"      : SCHEDULE_INTERVAL_DAILY, 
                                                        "SCHEDULE_TIME"          : "00:00:00"}#HH:MM:SS
                        }
}
###################################################################################################################################
