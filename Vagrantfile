$script = <<-SCRIPT
echo 'Updating package repos and updating packages.'
sudo apt-get update && sudo apt-get -y upgrade

echo 'Installing pyenv and python dependencies.'
sudo apt-get install -y --no-install-recommends build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git make build-essential libxmlsec1-dev libxml2-dev libsqlite3-dev

echo 'Cloning pyenv repo.'
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
cd ~/.pyenv && src/configure && make -C src

echo 'Defining environment variable PYENV_ROOT'
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile

echo 'Add pyenv init to shell'
echo 'eval "$(pyenv init --path)"' >> ~/.bash_profile
source ~/.bash_profile


echo 'Installing python.'
pyenv install 3.9.4
pyenv global 3.9.4

echo 'Installing poetry.'
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

SCRIPT

$app_setup = <<-SCRIPT
cd /vagrant

echo 'Installing TO-DO App dependencies.'
poetry install

echo ' Launching App.'
sudo -u vagrant poetry run gunicorn --daemon -b 0.0.0.0:5000 'todo_app.app:create_app()'

SCRIPT

Vagrant.configure("2") do |config|
    config.vm.box = "hashicorp/bionic64"
    config.vm.provision "shell", privileged: false, inline: $script
    
    config.vm.network "forwarded_port", guest: 5000, host:5000

    config.trigger.after :up do |trigger|
        trigger.name = "Launching App"
        trigger.info = "Running the TO-DO App setup script"
        trigger.run_remote = {privileged: false, inline: $app_setup}
    end
end
