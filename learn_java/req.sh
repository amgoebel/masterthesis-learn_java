sudo apt update
sudo apt install -y software-properties-common build-essential libffi-dev libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev libssl-dev
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install -y python3.12 python3.12-venv python3.12-distutils libxcb-cursor0
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.12 get-pip.py
python3.12 -m pip install pyqt6 bcrypt python-dotenv langchain-openai langchain-community langchainhub cffi
export OPENAI_API_KEY=sk-proj-0KMQeINNnl2EU3f50CLVT3BlbkFJTJqRvYtm3xgqS95M4Hh3
