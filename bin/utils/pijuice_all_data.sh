#!/bin/sh -x
python3 bin/utils/pijuice_log.py
python3 bin/utils/pijuice_util.py --dump
python3 bin/utils/pijuice_status.py
