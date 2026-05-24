Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  config.vm.define "broker" do |broker|
    broker.vm.hostname = "broker"
    broker.vm.network "private_network", ip: "192.168.56.10", virtualbox__intnet: "sd-net"
    broker.vm.provider "virtualbox" do |vb|
      vb.name   = "sd06-broker"
      vb.memory = "1024"
      vb.cpus   = 1
      vb.customize ["modifyvm", :id, "--usb", "off"]
      vb.customize ["modifyvm", :id, "--usbehci", "off"]
    end
    broker.vm.provision "shell", path: "setup/setup-broker.sh"
  end

  config.vm.define "produtor" do |produtor|
    produtor.vm.hostname = "produtor"
    produtor.vm.network "private_network", ip: "192.168.56.11", virtualbox__intnet: "sd-net"
    produtor.vm.provider "virtualbox" do |vb|
      vb.name   = "sd06-produtor"
      vb.memory = "512"
      vb.cpus   = 1
      vb.customize ["modifyvm", :id, "--usb", "off"]
      vb.customize ["modifyvm", :id, "--usbehci", "off"]
    end
    produtor.vm.provision "shell", path: "setup/setup-produtor.sh"
  end

  config.vm.define "consumidor" do |consumidor|
    consumidor.vm.hostname = "consumidor"
    consumidor.vm.network "private_network", ip: "192.168.56.12", virtualbox__intnet: "sd-net"
    consumidor.vm.provider "virtualbox" do |vb|
      vb.name   = "sd06-consumidor"
      vb.memory = "512"
      vb.cpus   = 1
      vb.customize ["modifyvm", :id, "--usb", "off"]
      vb.customize ["modifyvm", :id, "--usbehci", "off"]
    end
    consumidor.vm.provision "shell", path: "setup/setup-consumidor.sh"
  end

end