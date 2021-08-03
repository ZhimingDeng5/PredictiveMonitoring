import os
import uvicorn
from services.queue_controller import subscribeToInputQueue

node_class = os.environ['NODECLASS']

if node_class == "master":
    uvicorn.run('main_master:app', host='0.0.0.0', port=8000, workers=1)
elif node_class == "worker":
    subscribeToInputQueue()