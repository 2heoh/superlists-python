import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/2heoh/superlists-python.git'

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'  
    run(f'mkdir -p {site_folder}') 
    with cd(site_folder):  
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        _enable_nginx_site()
        _enable_service()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f"echo {REPO_URL}")
        run(f"git clone {REPO_URL} .")
        current_commit = local('git log -n 1 --format=%H', capture=True)
        run(f"git reset --hard {current_commit}")

def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python3.6 -m venv virtualenv')
    run('pwd')
    run('./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
    run('./virtualenv/bin/python3.6 manage.py collectstatic --noinput')

def _update_database():
    run('./virtualenv/bin/python3.6 manage.py migrate --noinput')

def _enable_nginx_site():
    run(f"sudo cp /home/{env.user}/sites/{env.host}/deploy_tools/nginx.template.conf /etc/nginx/sites-available/{env.host}")
    run(f"sudo sed -i 's/USER/{env.user}/g' /etc/nginx/sites-available/{env.host}")
    run(f"sudo sed -i 's/DOMAIN/{env.host}/g' /etc/nginx/sites-available/{env.host}")
    if not exists(f"/etc/nginx/sites-enabled/{env.host}"):
        run(f"sudo ln -s /etc/nginx/sites-available/{env.host} /etc/nginx/sites-enabled/{env.host}")

def _enable_service():
    run(f"sudo cp /home/{env.user}/sites/{env.host}/deploy_tools/gunicorn-template.service /etc/systemd/system/gunicorn-{env.host}.service")
    run(f"sudo sed -i 's/USER/{env.user}/g' /etc/systemd/system/gunicorn-{env.host}.service")
    run(f"sudo sed -i 's/DOMAIN/{env.host}/g' /etc/systemd/system/gunicorn-{env.host}.service")
