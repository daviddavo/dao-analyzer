# DAO-Analyzer
It is a tool to visualize DAO metrics. Currently, it shows DAO from [DAOstack](https://daostack.io/), [DAOhaus](https://daohaus.club/), and [Aragon](https://aragon.org/). Web site: [http://dao-analyzer.science/](http://dao-analyzer.science/)

## Architecture
There is available a class diagram of the [DAOstack app](https://github.com/Grasia/dao-analyzer/blob/master/src/apps/daostack/class_diagram.png), the [DAOhaus app](https://github.com/Grasia/dao-analyzer/blob/master/src/apps/daohaus/class_diagram.png), and the [Aragon app](https://github.com/Grasia/dao-analyzer/blob/master/src/apps/aragon/class_diagram.png).

## Using Docker
If you use Docker, you can just use the images at [grasia/dao-analyzer](https://hub.docker.com/r/grasia/dao-analyzer). The tags with the `-cached` suffix have a pre-populated data warehouse (this means the image uses more space, but takes less time to load). To use it, just run the command:

```
docker run -p80:80 grasia/dao-analyzer:latest
```

or

```
docker run -p80:80 grasia/dao-analyzer:latest-cached
```

## Download
Enter in your terminal (git must be installed) and write down:

`git clone https://github.com/Grasia/dao-analyzer`

After that, move to repository root directory with:

`cd dao-analyzer`

## Installation
All code has been tested on Linux, but it should work on Windows and macOS, 'cause it just uses the python environment.

So, you must install the following dependencies to run the tool:

* python3 (3.7 or later)
* python3-pip
* virtualenv (not essential)

Now, install the Python dependencies:

`pip3 install -r requirements.txt`

If you don't want to share Python dependencies among other projects, you should use a virtual environment, such as [virtualenv](https://docs.python-guide.org/dev/virtualenvs/).

At first, create a folder where you are going to install all Python dependencies:

`virtualenv -p python3 venv/`

Now, you have to activate it:

`source venv/bin/activate`

Finally, you can install the dependencies:

`pip install -r requirements.txt`

## How to run it?
Before launch the app, you have to run the following script in order to enable the cache stored in `datawarehouse`:

`python3 cache_scripts/main.py`

After a few minutes, you can now run the app with:

`python3 index.py`

Now, visit `http://127.0.0.1:8050` in your web browser.

### Debug mode
Setting the environment variable, `DEBUG`, before running the app, will enable the debug mode.

`export DEBUG=TRUE`

## How to test it?
Run all tests with:

`pytest`

or

`python3 -m pytest test/`

### Flags for hypothesis testing
Use this flag `--hypothesis-show-statistics` to show statistics.

Use the flag `--hypothesis-seed=<int>` to set a fixed seed, it's useful to reproduce a failure.

## Deploy
In order to fully deploy the app, use the `deploy.sh` script, which installs all the Python dependencies, updates the datawarehouse, and runs the web-app with gunicorn, using the `gunicorn_config.py` file.

## Publications
* Faqir-Rhazoui, Youssef, Javier Arroyo Gallardo, and Samer Hassan. "A Scalable Voting System: Validation of Holographic Consensus in DAOstack." (2020).
    * [Freely available here](https://eprints.ucm.es/id/eprint/62303/).

* El Faqir, Y., Arroyo, J., Hassan, S. (2020). An overview of Decentralized Autonomous Organizations on the blockchain. Proceedings of the 16th International Symposium on Open Collaboration (Opensym 2020) 11:1-11:8. ACM. 
    * [Freely available here](https://opensym.org/wp-content/uploads/2020/08/os20-paper-a11-el-faqir.pdf).

## Acknowledgements
This work is funded by the Spanish Ministry of Science and Innovation and the [P2P Models](https://p2pmodels.eu/) project, which is funded by the European Research Council.