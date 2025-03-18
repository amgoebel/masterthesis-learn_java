sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt install -y software-properties-common build-essential libffi-dev libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev libssl-dev python3.12 python3.12-venv libxcb-cursor0
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.12 get-pip.py
python3.12 -m pip install pyqt6==6.7.1 bcrypt==4.2.1 cryptography==44.0.0 python-dotenv langchain-openai langchain-anthropic langchain-community langchainhub cffi==1.17.1
echo "All requirements have been installed."
