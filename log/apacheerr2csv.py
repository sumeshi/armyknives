#!/usr/bin/env python3
# apacheerr2csv.py
# usage: python apacheerr2csv.py input.log output.csv
import re
import csv
import sys

if len(sys.argv) > 2:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
else:
    raise Exception("No input file or output file specified")

headers = """timestamp,loc,type,sn,lv,evt,subEvt,os,com,domain,profile,tmid,csid,
ip,mac,channel,evtRecID,evtID,evtMsg,evtSrc,evtPsID,evtUsr,evtDomain,evtLogonID,
logonType,wsName,wsIp,wsPort,usr,usrDomain,srcCom,srcIP,srcPort,sessionID,psGUID,
psPath,dstIP,dstPort,recv,send,errCode,targetUsr,targetDomain,targetService,
ticketOption,ticketStatus,privList,cmd,psID,psUser,psDomain,arc,sha256,sha1,md5,
company,copyright,fileDesc,fileVer,product,productVer,crTime,acTime,moTime,size,
sig,signer,issuer,cerSN,validFrom,validTo,sTime,path,drvType,read,write,mmf,pe,
new,entry,valType,valStr,valNum,valOldNum,rf,rcCom,rcIP,winTitle,activeTime,
hide,parentGUID,parentPath,clipType,clipData,spsGUID,spsPath,valSize,mntFld,
dstPath,dstMntFld,dstDrv,shCmd,cmdType,dstHost,ver,logVer,rs,trs,allow_url_include,
auto_prepend_file,packed,impKrnlCnt,brType,url,decode""".replace("\n", "").split(",")

headers = [h.strip() for h in headers]

log_pattern = re.compile(
    r'^\s*\[(?P<timestamp>[^\]]+)\]\s+'
    r'\[(?P<module>[^\]]+)\]\s+'
    r'\[pid\s+(?P<pid>\d+):tid\s+(?P<tid>\d+)\]\s+'
    r'\[client\s+(?P<client_ip>[^:\]]+):(?P<client_port>\d+)\]\s*'
    r'(?P<msg>.*)$'
)

def safe_prefix(key, value):
    if not value or value == "-":
        return ""
    return f"[apache.{key}]{value.strip()}"

with open(input_file, "r", encoding="utf-8", errors="replace") as infile, \
     open(output_file, "w", newline="", encoding="utf-8") as outfile:

    writer = csv.DictWriter(outfile, fieldnames=headers)
    writer.writeheader()

    for line in infile:
        line = line.rstrip("\n")
        m = log_pattern.match(line)
        if not m:
            continue
        d = m.groupdict()
        row = {h: "" for h in headers}

        row["timestamp"] = d["timestamp"] + " +0900"
        row["ip"] = safe_prefix("client_ip", d["client_ip"])
        row["srcIP"] = row["ip"]
        row["srcPort"] = safe_prefix("client_port", d["client_port"])
        row["evtRecID"] = safe_prefix("pid", d["pid"])
        row["evtID"] = safe_prefix("tid", d["tid"])
        row["evtSrc"] = safe_prefix("module", d["module"])
        row["evtMsg"] = safe_prefix("msg", d["msg"])

        m_path = re.search(r'([A-Za-z]:[\\/][^\s:]+)', d["msg"])
        if m_path:
            path = m_path.group(1)
            row["path"] = safe_prefix("path", path)
            row["dstPath"] = safe_prefix("dstPath", path)
            row["brType"] = safe_prefix("exe", path.split("\\")[-1].split("/")[-1])

        writer.writerow(row)
