# soliton
cat *.log | sort > soliton.csv
python3 soliton2csv.py soliton.log soliton.csv
python3 change_dateformat_csv.py soliton.csv soliton2.csv timestamp soliton

# squid-access
python3 squid2csv.py access.log access.csv
python3 change_dateformat_csv.py access.csv access.csv timestamp squid_access

# apache-error
python3 apacheerr2csv.py error.log error.csv
python3 change_dateformat_csv.py error.csv error2.csv timestamp apache_error

# merge
python3 merge_sameheader_csvs.py soliton2.csv access.csv error2.csv merged.csv

# remove unused cols
python3 delete_unused_cols.py merged.csv simplified.csv loc,type,os,domain,profile