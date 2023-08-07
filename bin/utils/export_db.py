import sys
import db

if len(sys.argv)>1:
    db.db_show_data_from(sys.argv[1])
else:
    db.db_export_all_data_to_csv("data_Logs")


