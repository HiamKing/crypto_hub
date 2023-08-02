For the project installation, you can follow these steps:

1. You need to first have install Docker and Docker compose. If your computer haven't installed Docker and Docker compose, you can refer to this link for the installation [link1](https://docs.docker.com/engine/install/ubuntu/), [link2](https://docs.docker.com/compose/install/).

2. You need to create folder for every volumes section in the docker-compose.yml file. You also need to set hostname for the ip of all container in your computer too.

3. Run `docker-compose up -d` in the main project.

There are 4 separated modules in this project: data_collector, data_consumer.batching, data_consumer.streaming, data_loader. Each module have 2 apps for Binance and CoinMarketCap so you will need to start total 8 services. Next, you will need to follow below steps for each of module:

1. Go to /src dir by `cd /src`

2. Create a virtual python env (python 3.10.4), activate it and run `pip install -r /<module_path>/requirements.txt`.

3. Run `python -m applications.<binance_app_module>.app`.

4. Run `python -m applications.<coinmarketcap_app_module>.app`.

Next, you will need to run server and UI of the project by:

1. Create a virtual python env (python 3.10.4) for server, activate it and run `pip install -r /server/requirements.txt`.

2. Start the server by the command `flask run`.

3. Go to the UI directory by `cd ui/` and install UI dependencies by the command `npm install`.

4. Start the UI by the command `REACT_APP_API_ROOT=http://127.0.0.1:5000 npm start`.

Now your project should start and run smoothly.
