Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  config.vm.define "server" do |server|
    server.vm.hostname = "server"
    server.vm.network "private_network", ip: "192.168.56.10"
    server.vm.provider "virtualbox" do |vb|
      vb.name   = "sd03-server"
      vb.memory = "512"
      vb.cpus   = 2
    end
    server.vm.provision "shell", path: "setup/setup-server.sh"
  end

  config.vm.define "client" do |client|
    client.vm.hostname = "client"
    client.vm.network "private_network", ip: "192.168.56.11"
    client.vm.provider "virtualbox" do |vb|
      vb.name   = "sd03-client"
      vb.memory = "512"
      vb.cpus   = 1
    end
    client.vm.provision "shell", path: "setup/setup-client.sh"
  end
end
