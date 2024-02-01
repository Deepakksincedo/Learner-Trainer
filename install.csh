deactivate
git reset --hard
sudo git clean -fxd
git pull
virtualenv .envDev
source .envDev/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
sudo .envDev/bin/python3 manage.py runserver 0.0.0.0:80