# go to util directory and run python db_init.py
echo "Please revise this script to change string ~/base to a dir determined by ../config.py"
pip install sqlalchemy
mkdir ~/base
cd ../utils
python db_init.py
