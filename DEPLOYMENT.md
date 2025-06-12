# 🚀 Quick Deployment Guide

## Prerequisites
- VirtualBox installed
- Vagrant installed
- Internet connection for downloading packages

## Step-by-Step Deployment

### 1. Start the VMs
```bash
# Navigate to the project directory
cd devops-lab

# Start all VMs (this will some minutes)
vagrant up
```

### 2. Deploy the Application Stack
```bash
# SSH into the Ansible controller
vagrant ssh main

# Navigate to the ansible directory
cd /vagrant/ansible

# Run the complete deployment
ansible-playbook playbooks/site.yml
```

### 3. Access the Application
Open your browser and go to: **http://localhost:8080**

## 🛠️ Development Commands

### Individual Component Deployment
```bash
vagrant ssh main
cd /vagrant/ansible

# Deploy only common configuration
ansible-playbook playbooks/site.yml --tags="common"

# Deploy only database server
ansible-playbook playbooks/site.yml --tags="db"

# Deploy only Docker setup
ansible-playbook playbooks/site.yml --tags="docker"

# Deploy only the Flask application
ansible-playbook playbooks/site.yml --tags="app"
```

### Container Management
```bash
# Check container status
vagrant ssh main
ansible web -m shell -a "cd /opt/devops_lab && docker compose ps"

# View application logs
ansible web -m shell -a "cd /opt/devops_lab && docker compose logs flask_app"

# Restart application
ansible web -m shell -a "cd /opt/devops_lab && docker compose restart"

# Rebuild and restart
ansible web -m shell -a "cd /opt/devops_lab && docker compose up --build --detach"
```

### Database Operations
```bash
# Connect to PostgreSQL
vagrant ssh main
ansible db -m shell -a "sudo -u postgres psql devops_lab"

# Check database tables
ansible db -m shell -a "sudo -u postgres psql devops_lab -c '\dt'"

# View visitor data
ansible db -m shell -a "sudo -u postgres psql devops_lab -c 'SELECT * FROM visitors;'"
```

## 🔧 Troubleshooting

### VM Issues
```bash
# Check VM status
vagrant status

# Restart specific VM
vagrant reload web

# SSH into specific VM
vagrant ssh web
```

### Network Issues
```bash
# Check port forwarding
vagrant port

# Test connectivity between VMs
vagrant ssh main
ansible all -m ping
```

### Application Issues
```bash
# Check if containers are running
vagrant ssh main
ansible web -m shell -a "docker ps"

# Check container logs
ansible web -m shell -a "docker logs flask_app"
ansible web -m shell -a "docker logs nginx_proxy"

# Check application health
curl http://localhost:8080/health
```

### Database Issues
```bash
# Check PostgreSQL status
vagrant ssh main
ansible db -m shell -a "systemctl status postgresql"

# Test database connectivity
ansible db -m shell -a "sudo -u postgres pg_isready"

# Check database configuration
ansible db -m shell -a "sudo -u postgres psql -c 'SHOW listen_addresses;'"
```

## 🧹 Cleanup

### Stop and Remove Everything
```bash
# Destroy all VMs
vagrant destroy -f

# Remove Vagrant box (if you want to)
vagrant box remove ubuntu/jammy64
```

### Restart Fresh
```bash
# Start over with clean VMs
vagrant destroy -f
vagrant up
vagrant ssh main
cd /vagrant/ansible
ansible-playbook playbooks/site.yml
```

## 📊 Monitoring URLs

- **Main Application**: http://localhost:8080
- **Application Health**: http://localhost:8080/health
- **API Statistics**: http://localhost:8080/api/stats
- **Nginx Health**: http://localhost:8080/nginx-health
- **Direct Flask Access**: http://localhost:5000 (this bypasses Nginx)

## 🎯 Success Indicators

✅ All VMs running and accessible  
✅ Ansible can connect to all hosts  
✅ PostgreSQL service active on db-server  
✅ Docker service active on web-server  
✅ Flask and Nginx containers running  
✅ Web application accessible on port 8080  
✅ Database connectivity working  
✅ Health checks passing  

**Hope this helps! 🎓**
