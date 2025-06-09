Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/focal64" # Ubuntu 20.04 LTS
    config.vm.provider "virtualbox" do |vb| # We are using Virtual Box on our Windows Machine
        vb.memory = "1024"
        vb.cpus = 1
    end

    # Shared provision for all VMs, where we are updating the package list
    config.vm.provision "shell", inline: <<-SHELL
        echo "Running system update..."
        sudo apt-get update
    SHELL

    # This will be our database VM hosting postgres SQL server
    config.vm.define "db" do |db|
        db.vm.hostname = "db-server"
        db.vm.network :private_network, ip:"192.168.61.11"
        db.vm.network "forwarded_port", guest: 22, host: 2223, id: "ssh"
    end

    # This will be our web VM with the web application
    config.vm.define "web" do |web|
        web.vm.hostname = "web-server"
        web.vm.network :private_network, ip:"192.168.61.12"
        web.vm.network "forwarded_port", guest: 22, host: 2224, id: "ssh"
        web.vm.network "forwarded_port", guest: 80, host: 8080, id: "http"
    end

    # And finally is our main VM serving as the Ansible Controller
    # It is configured last, so it can access the other VMs' SSH keys
    config.vm.define "main" do |main|
        main.vm.hostname = "main-server" # always useful
        # We are defining the private network IP address.
        # This is the IP address that will be used to communicate between VMs!
        main.vm.network :private_network, ip:"192.168.61.10"
        # We are forwarding port 22 of the guest VM to port 2222 on the host machine.
        # This allows us to SSH into the VM using `ssh -p 2222 vagrant@localhost` from our windows machine.
        # You could also use `vagrant ssh main` to SSH into the VM.
        main.vm.network "forwarded_port", guest: 22, host: 2222, id: "ssh"
        
        # Now since we love automation, we are already installing ansible on our Controller VM
        # and settings up the SSH keys for the other VMs so that Ansible can connect to them
        # ATTENTION: We are using `privileged: false` to run the script as the vagrant user not as the root user.
        # This is important because we want to create the SSH keys in the vagrant user's home directory.
        main.vm.provision "shell", privileged: false, inline: <<-SHELL
        # Create secure directory for SSH keys
        mkdir -p /home/vagrant/.ssh/keys
        chmod 700 /home/vagrant/.ssh/keys
        
        # Copy and secure keys
        cp /vagrant/.vagrant/machines/db/virtualbox/private_key /home/vagrant/.ssh/keys/db_key
        cp /vagrant/.vagrant/machines/web/virtualbox/private_key /home/vagrant/.ssh/keys/web_key
        chmod 600 /home/vagrant/.ssh/keys/*
        
        echo "SSH keys secured and ready for Ansible"

        # Create ansible.cfg in the vagrant user's home directory
        cat > /home/vagrant/.ansible.cfg << EOF
[defaults]
inventory = /vagrant/ansible/inventory.yml
remote_user = vagrant
host_key_checking = False
interpreter_python = /usr/bin/python3
roles_path = /vagrant/ansible/roles

[ssh_connection]
pipelining = True
EOF
        
        echo "Ansible configuration created in /home/vagrant/.ansible.cfg"
        SHELL

        # Install Ansible as root (since package installation requires root)
        main.vm.provision "shell", inline: <<-SHELL
        echo "Installing Ansible..."
        apt-get install -y ansible
        # Install Ansible collections
        ansible-galaxy collection install community.general
        ansible-galaxy collection install community.postgresql
        echo "Ansible installed!"
        su - vagrant -c "ansible --version"
        SHELL
    end


    config.vm.post_up_message = "
    The VM is ready!
    "
end