#!/usr/bin/env python3
# squid2csv.py
# usage: python squid2csv.py input.log output.csv

import re
import csv
import sys
from urllib.parse import urlparse

if len(sys.argv) > 2:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
else:
    raise Exception("No input file or output file specified")

log_pattern = re.compile(
    r'(?P<client_ip>\S+)\s+'
    r'(?P<ident>\S+)\s+'
    r'(?P<user>\S+)\s+'
    r'\[(?P<timestamp>[^\]]+)\]\s+'
    r'"(?P<method>[A-Z]+)\s+(?P<url>\S+)\s+HTTP/(?P<protocol>[^"]+)"\s+'
    r'(?P<http_status>\d+)\s+'
    r'(?P<reply_size>\S+)\s+'
    r'"(?P<referer>[^"]*)"\s+'
    r'"(?P<user_agent>[^"]*)"?\s*'
    r'(?:(?P<cache_status>[^:]+):(?P<hierarchy>\S+))?'
)

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

def safe_prefix(key, value):
    if value is None:
        return ""
    v = str(value).strip()
    if v == "" or v == "-":
        return ""
    return f"[squid.{key}]{v}"

with open(input_file, "r", encoding="utf-8", errors="replace") as infile, \
     open(output_file, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=headers)
    writer.writeheader()

    for line in infile:
        line = line.rstrip("\n")
        if not line:
            continue

        match = log_pattern.match(line)
        if not match:
            print("Parse failed:", line)
            continue

        d = match.groupdict()
        row = {h: "" for h in headers}

        ts = d.get("timestamp", "")
        row["timestamp"] = ts

        row["ip"] = safe_prefix("client_ip", d.get("client_ip", ""))

        row["usr"] = safe_prefix("user", d.get("user", ""))

        row["url"] = safe_prefix("url", d.get("url", ""))

        method = d.get("method", "") or ""
        url = d.get("url", "") or ""
        evt_msg_parts = []
        if method and method != "-":
            evt_msg_parts.append(f"[squid.method]{method}")
        if url and url != "-":
            evt_msg_parts.append(f"[squid.url]{url}")
        row["evtMsg"] = " ".join(evt_msg_parts)

        status = d.get("http_status", "")
        row["rs"] = safe_prefix("status", status)

        row["recv"] = safe_prefix("size", d.get("reply_size", ""))

        row["brType"] = safe_prefix("ua", d.get("user_agent", ""))

        cache = d.get("cache_status") or ""
        hier = d.get("hierarchy") or ""
        cache = cache.strip()
        hier = hier.strip()
        if cache or hier:
            row["decode"] = f"[squid.cache]{cache}:{hier}"
        else:
            row["decode"] = ""

        ref = d.get("referer", "")
        if ref and ref != "-":
            try:
                parsed = urlparse(ref)
                netloc = parsed.netloc or ""
                if netloc:
                    row["domain"] = f"[squid.referer]{netloc}"
                row["path"] = f"[squid.referer_path]{ref}"
            except Exception:
                row["path"] = f"[squid.referer_path]{ref}"

        writer.writerow(row)
