import os
import json
import uuid
import socket
import shutil
import psutil
import logging
import datetime
import humanize
import platform
import pyminizip
import subprocess as sp
import logging.handlers

import config as conf

from collections import OrderedDict 

def get_logger(logger_path):
    logger = logging.getLogger()
    formatter = logging.Formatter("[%(asctime)s - %(levelname)s]: %(message)s")
    
    if not logger_path:
        raise Exception("logger path not specified")
    logger_dir = os.path.dirname(logger_path)
    if not os.path.exists(logger_dir):
        os.makedirs(logger_dir)
    logger_name = os.path.basename(os.path.splitext(logger_path)[0])
    logger = logging.getLogger(logger_name)
    fileHandler = logging.handlers.RotatingFileHandler(logger_dir+ os.path.sep + logger_name + ".log", maxBytes=1*1024*1024*1021, backupCount=2)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    logger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    return logger

logger = get_logger(conf.LOG_PATH)

def get_host_name():
    return socket.gethostname()

def pyminizip_compressor(dst_zip_file, project_configuration, log_dump=True, mongo_dump=True, sys_log_dump=True, password=None, compress_level=9):
    logger.info("[pyminizip_compressor][Utils][Using pyminizip compressor]")
    src_files_list = []
    arc_names_list = []
    
    remove_files = []
    
    try:
        if log_dump:
            log_files, log_arc_names = get_logs(project_configuration)

            src_files_list.extend(log_files)
            arc_names_list.extend(log_arc_names)

        if mongo_dump:
            mongo_dump_files, mongo_dump_arc_names, remove_folder = get_mongodump(project_configuration)
            src_files_list.extend(mongo_dump_files)
            arc_names_list.extend(mongo_dump_arc_names)
            if remove_folder:
                remove_files.append(remove_folder)

        if sys_log_dump:
            sys_dump_files, sys_dump_arc_names, remove_file = get_sys_info_log(project_configuration)
            src_files_list.extend(sys_dump_files)
            arc_names_list.extend(sys_dump_arc_names)
            if remove_file:
                remove_files.extend(remove_file)
        
        par_arc_dirs = [os.path.dirname(arc_path) for arc_path in arc_names_list ]

        pyminizip.compress_multiple(src_files_list, par_arc_dirs, dst_zip_file, password, compress_level)  
    except Exception as ex:
        logger.exception("[zipfile_compressor][Utils][Exception->{}]".format(ex))
    
    for file_ in  remove_files:
        if os.path.exists(file_):
            if os.path.isdir(file_):
                shutil.rmtree(file_)
            else:
                os.remove(file_)


def zipfile_compressor(zip_f, project_configuration, writer, log_dump=True, mongo_dump=True, sys_log_dump=True):
    src_files_list = []
    arc_names_list = []
    
    remove_files = []
    
    try:
        if log_dump:
            log_files, log_arc_names = get_logs(project_configuration)

            src_files_list.extend(log_files)
            arc_names_list.extend(log_arc_names)

        if mongo_dump:
            mongo_dump_files, mongo_dump_arc_names, remove_folder = get_mongodump(project_configuration)
            src_files_list.extend(mongo_dump_files)
            arc_names_list.extend(mongo_dump_arc_names)
            if remove_folder:
                remove_files.append(remove_folder)

        if sys_log_dump:
            sys_dump_files, sys_dump_arc_names, remove_file = get_sys_info_log(project_configuration)
            src_files_list.extend(sys_dump_files)
            arc_names_list.extend(sys_dump_arc_names)
            if remove_file:
                remove_files.extend(remove_file)

        for i in range(0, len(src_files_list)):
            writer(src_files_list[i], arcname= arc_names_list[i])

    except Exception as ex:
        logger.exception("[zipfile_compressor][Utils][Exception->{}]".format(ex))
    
    for file_ in  remove_files:
        if os.path.exists(file_):
            if os.path.isdir(file_):
                shutil.rmtree(file_)
            else:
                os.remove(file_)

def get_logs(project_configuration):
    log_files = []
     
    for file_ in project_configuration["LOG_FILES"]:
        path = os.path.join(project_configuration["LOG_PATH"], file_)
        if os.path.exists(path):
            log_files.append(path)
    
    if os.name == "posix":
        if os.path.exists(project_configuration["SUPERVISOR_LOG_PATH"]):
            for file_ in os.listdir(project_configuration["SUPERVISOR_LOG_PATH"]):
                if file_.startswith(project_configuration["SUPERVISOR_LOG_FILES"]) and file_.endswith(".log"):
                    log_files.append(os.path.join(project_configuration["SUPERVISOR_LOG_PATH"], file_))
    
    logger.info("[get_logs][Utils][Logs to Download->{}]".format(",".join(log_files)))
    
    arc_names_list = []
    for file_ in log_files:
        arc_names_list.append(os.path.join("/logs", os.path.basename(file_)) )
    
    return log_files, arc_names_list
    

def get_mongodump(project_configuration):
    host = project_configuration["MONGO_DB_IP"] if type(project_configuration["MONGO_DB_IP"]) in [str, bytes] else project_configuration["MONGO_DB_IP"][0]
    output_dir_path = os.path.join(conf.DUMP_FOLDER_PATH, datetime.datetime.now().strftime("%d_%m_%Y"))
    output_path = os.path.join(output_dir_path, str(uuid.uuid4()), "dump")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    dump_command = [conf.MONGODUMP_BINARY_FILE, "--db", project_configuration["DB_NAME"], "--host", host, "--port", project_configuration["MONGO_DB_PORT"], "--out", output_path]

    if project_configuration["DB_AUTHENTICATION"]:
        dump_command.extend(["--username", project_configuration["DB_USERNAME"], "--password", project_configuration["DB_PASSWORD"]])

    
    p = sp.Popen(dump_command)
    while p.poll() is None:
        try:
            logger.info("[get_mongodump][Utils][{}]".format(p.stdout.read()))
        except:
            pass
    
    if p.returncode == 0:
        src_files_list = []
        arc_names_list = []
        for root, dirs, files in os.walk(output_path):
            for file_ in files:
                zip_dump_path = os.path.join("dump", project_configuration["DB_NAME"], file_)
                
                src_files_list.append(os.path.join(root, file_))
                arc_names_list.append("/"+zip_dump_path)
        
 
        return src_files_list, arc_names_list, output_dir_path

def get_machine_info():
    info = OrderedDict()
    uname = platform.uname()    
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
    
    info["System"] = uname.system
    info["Node Name"] = uname.node
    info["Release"] = uname.release
    info["Version"] = uname.version
    info["Machine"] = uname.machine
    info["Processor"] = uname.processor
    info["Up time"] = "{}/{}/{} {}:{}:{}".format(bt.day, bt.month, bt.year, bt.hour, bt.minute, bt.second)
    info["Up time epoch"] = boot_time_timestamp

    return info

def get_cpu_info():
    info = OrderedDict()
    
    info["Physical cores"] = psutil.cpu_count(logical=False)
    info["Total cores"] = psutil.cpu_count(logical=True)
     
    cpufreq = psutil.cpu_freq()
    
    info["Max Frequency"] = "{}Mhz".format(cpufreq.max)
    info["Min Frequency"] = "{}Mhz".format(cpufreq.min)
    info["Current Frequency"] = "{}Mhz".format(cpufreq.current)
    info["CPU Usage Per Core"] = OrderedDict()

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        info["CPU Usage Per Core"]["Core {}".format(i)] = "{}%".format(percentage)

    info["Total CPU Usage"] = psutil.cpu_percent()

    return info


def get_mem_info():
    info = OrderedDict()
       
    svmem = psutil.virtual_memory()

    info["Total"] = humanize.naturalsize(svmem.total)
    info["Available"] = humanize.naturalsize(svmem.available)
    info["Used"] = humanize.naturalsize(svmem.used)
    info["Percentage"] = "{}%".format(svmem.percent)
    return info

def get_swap_mem_info():
    info = OrderedDict()

    swap = psutil.swap_memory()
    
    info["Total"] = humanize.naturalsize(swap.total)
    info["Free"] = humanize.naturalsize(swap.free)
    info["Used"] = humanize.naturalsize(swap.used)
    info["Percentage"] = "{}%".format(swap.percent)

    return info
    

def get_sys_info_log(project_configuration):
    system_info = {"info":{}, "disk_info":{"disks": []}, "network_info":{"networks":[]},"cpu_info":{},"mem_info":{},"date":datetime.datetime.now().strftime("%d-%m-%Y__%H_%M_%S")}
    
    system_info_txt = "{}\n{}System Information{}\n".format("="*130,"="*40,"="*40)
    machine_info = get_machine_info()
    
    for key, val in machine_info.items():
        system_info_txt += "{}: {}\n".format(key, val)
    
    system_info["info"].update(machine_info) 
  

    system_info_txt += "\n{}CPU Info{}\n".format("="*40,"="*40)
    cpu_info = get_cpu_info()

    for key, val in cpu_info.items():
        if type(val) in [OrderedDict, dict]:
            system_info_txt += "{}:\n".format(key)
            for key, value in val.items():
                system_info_txt += "   {}: {}\n".format(key, value)
        else:
            system_info_txt += "{}: {}\n".format(key, val)

    system_info["cpu_info"].update(cpu_info)


    system_info_txt += "\n{}Memory Info{}\n".format("="*40,"="*40)
    mem_info = get_mem_info()

    for key, val in mem_info.items():
        system_info_txt += "{}: {}\n".format(key, val)
    
    system_info_txt += "\n{}SWAP{}\n".format("="*20,"="*20)
    swap_mem_info = get_swap_mem_info()
    for key, val in swap_mem_info.items():
        system_info_txt += "{}: {}\n".format(key, val)
    
    system_info["mem_info"].update(mem_info)
    system_info["mem_info"].update(swap_mem_info)
    
    system_info_txt += "\n{}Disk Info{}\nPartitions and Usage:\n".format("="*40,"="*40)
    partitions = psutil.disk_partitions()

    for partition in partitions:
        system_info_txt += "\n=== Device: {} ===\n".format(partition.device)
        system_info_txt += "   Mountpoint: {} \n".format(partition.mountpoint)
        system_info_txt += "   File system type: {} \n".format(partition.fstype)

        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue

        system_info_txt += "   Total Size: {} \n".format(humanize.naturalsize(partition_usage.total))
        system_info_txt += "   Used: {} \n".format(humanize.naturalsize(partition_usage.used))
        system_info_txt += "   Free: {} \n".format(humanize.naturalsize(partition_usage.free))
        system_info_txt += "   Percentage: {}% \n".format(partition_usage.percent)

        system_info["disk_info"]["disks"].append({"Device": partition.device,
                                                    "Mountpoint": partition.mountpoint,
                                                    "File system type": partition.fstype,
                                                    "Total Size": partition_usage.total,
                                                    "Used": partition_usage.used,
                                                    "Free": partition_usage.free,
                                                    "Percentage": partition_usage.percent})
    
    disk_io = psutil.disk_io_counters()

    system_info_txt += "\nTotal read: {} ===\n".format(humanize.naturalsize(disk_io.read_bytes))
    system_info_txt += "Total write: {} ===\n".format(humanize.naturalsize(disk_io.write_bytes))

    system_info["disk_info"]["Total read"] = disk_io.read_bytes
    system_info["disk_info"]["Total write"] = disk_io.write_bytes

    system_info_txt += "\n{}Network Info{}\n".format("="*40,"="*40)

    if_addrs = psutil.net_if_addrs()
    
    network_info = {}
    for interface_name, interface_addresses in if_addrs.items():
        network_info[interface_name] = []
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                system_info_txt += "\n=== Interface: {} ===\n".format(interface_name)
                system_info_txt += "  IP Address: {}\n".format(address.address)
                system_info_txt += "  Netmask: {}\n".format(address.netmask)
                system_info_txt += "  Broadcast IP: {}\n".format(address.broadcast)

                network_info[interface_name].append({"IP Address": address.address, "Netmask": address.netmask, "Broadcast IP": address.broadcast})

            elif str(address.family) == 'AddressFamily.AF_PACKET':
                system_info_txt += "\n=== Interface: {} ===\n".format(interface_name)
                system_info_txt += "  MAC Address: {}\n".format(address.address)
                system_info_txt += "  Netmask: {}\n".format(address.netmask)
                system_info_txt += "  Broadcast MAC: {}\n".format(address.broadcast)

                network_info[interface_name].append({"MAC Address": address.address, "Netmask": address.netmask, "Broadcast MAC": address.broadcast})

        system_info["network_info"]["networks"].append(network_info)

        
    net_io = psutil.net_io_counters()
        
    system_info_txt += "\nTotal Bytes Sent: {} ===\n".format(humanize.naturalsize(net_io.bytes_sent))
    system_info_txt += "Total Bytes Received: {} ===\n".format(humanize.naturalsize(net_io.bytes_recv))
    
    system_info["network_info"]["Total Bytes Sent"] = humanize.naturalsize(net_io.bytes_sent)
    system_info["network_info"]["Total Bytes Sent"] = humanize.naturalsize(net_io.bytes_recv)
    
    system_info_txt += "{}\n".format("*"*130)
    system_info_txt += "Generated on {}".format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))


    system_file_log = os.path.join(conf.DUMP_FOLDER_PATH,  "system_info_{}.log".format(datetime.datetime.now().strftime("%d-%m-%Y__%H_%M_%S")))
    system_file_json = os.path.join(conf.DUMP_FOLDER_PATH, "system_info_{}.json".format(datetime.datetime.now().strftime("%d-%m-%Y__%H_%M_%S")))
    
    with open(system_file_log,"w") as f:
        f.write(system_info_txt)

    with open(system_file_json,"w") as f:
        f.write(json.dumps(system_info))

    return [system_file_log,system_file_json],["/system_log/{}".format(os.path.basename(system_file_log)),"/system_log/{}".format(os.path.basename(system_file_json))], [system_file_log,system_file_json]
