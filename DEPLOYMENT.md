# Deploying to Hostinger VPS

Follow these steps to deploy your Django application to your VPS.

## 1. Connect to VPS
Open your terminal (PowerShell or CMD) and run:
```bash
ssh root@72.62.247.49
```
*(Enter your VPS password when prompted)*

## 2. Install Required Software
Run the following commands on the server to install Python, Nginx, and Git:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx git -y
```

## 3. Clone the Repository
Navigate to the web directory and clone your project:
```bash
cd /var/www
git clone https://github.com/Nanostack-Technologies/NanoStack-Technologies.git
cd NanoStack-Technologies
```

## 4. Set up Virtual Environment
Create and activate the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

## 5. Install Dependencies
Install all required Python packages:
```bash
pip install -r requirements.txt
pip install gunicorn
```

## 6. Configure Database & Static Files
Run Django migrations and collect static files:
```bash
python3 manage.py migrate
python3 manage.py collectstatic --noinput
```

## 7. Setup System Service (Gunicorn)
We will use the `gunicorn.service` file included in your repo.
```bash
sudo cp gunicorn.service /etc/systemd/system/
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## 8. Configure Nginx
We will use the `nginx_config` file included in your repo.
```bash
sudo cp nginx_config /etc/nginx/sites-available/nanostack
sudo ln -s /etc/nginx/sites-available/nanostack /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```

## 9. Final Check
Visit **http://72.62.247.49** in your browser. Your site should be live!

---

### Troubleshooting
If something doesn't work, check the logs:
```bash
sudo journalctl -u gunicorn
sudo tail -f /var/log/nginx/error.log
```
