Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  config.vm.define "nameserver" do |ns|
    ns.vm.hostname = "nameserver"
    ns.vm.network "private_network", ip: "192.168.56.10"
    ns.vm.provider "virtualbox" do |vb|
      vb.name   = "sd05-nameserver"
      vb.memory = "512"
      vb.cpus   = 1
      vb.customize ["modifyvm", :id, "--usb", "off"]
      vb.customize ["modifyvm", :id, "--usbehci", "off"]
    end
    ns.vm.provision "shell", path: "setup/setup-nameserver.sh"
  end

  config.vm.define "server" do |server|
    server.vm.hostname = "server"
    server.vm.network "private_network", ip: "192.168.56.11"
    server.vm.provider "virtualbox" do |vb|
      vb.name   = "sd05-server"
      vb.memory = "512"
      vb.cpus   = 1
      vb.customize ["modifyvm", :id, "--usb", "off"]
      vb.customize ["modifyvm", :id, "--usbehci", "off"]
    end
    server.vm.provision "shell", path: "setup/setup-server.sh"
  end

  config.vm.define "client" do |client|
    client.vm.hostname = "client"
    client.vm.network "private_network", ip: "192.168.56.12"
    client.vm.provider "virtualbox" do |vb|
      vb.name   = "sd05-client"
      vb.memory = "512"
      vb.cpus   = 1
      vb.customize ["modifyvm", :id, "--usb", "off"]
      vb.customize ["modifyvm", :id, "--usbehci", "off"]
    end
    client.vm.provision "shell", path: "setup/setup-client.sh"
  end
end