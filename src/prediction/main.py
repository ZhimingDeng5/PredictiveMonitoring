import os
import uvicorn
from main_worker import WorkerNode
from main_persistence import PersistenceNode

node_class = os.environ['NODECLASS']

if node_class == "master":
    uvicorn.run('main_master:app', host='0.0.0.0', port=8000, workers=1)
elif node_class == "worker":
    WorkerNode().start()
elif node_class == "persistence":
    PersistenceNode().start()
