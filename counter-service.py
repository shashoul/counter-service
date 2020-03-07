from flask import Flask, request
from threading import Lock
import redis
import os

"""
    date: 7 March 2020
    app name: counter-service

    The following flask app counts the amount of POST
    requests and return it on every GET request.
    The service can be run in two mode with redis (we should provide redis_host)
    and without redis( we using global variable and the data is just kept in memory ,
    and will be lost once the app is down or crashing.)
"""
app = Flask(__name__)
counter = 0
lock = Lock()

# check if redis host provided and establish a connection.
redis_up=False
redis_host = os.getenv("redis_host")
if redis_host != "":
    rediscache = redis.Redis(host=redis_host,
                port=os.getenv("redis_port"))
    redis_up=True


def counter_service_post():
    """
        Handling a POST request.
    """
    try:
        if redis_up:
            # if we running with redis, just increment counter.
            rediscache.incr('counter')
        else:
            global counter
            # using lock to prevent more than one thread to change the value of the counter.
            lock.acquire()
            counter += 1
            lock.release()
        return "{OK}", 200
    except:
        return "Internal Error, Please check redis connection", 500


def counter_service_get():
    """
        Handling a GET request.
    """
    try:
        if redis_up:
            # if we running with redis
            web_server_counter = rediscache.get('counter')
            if web_server_counter is None:
                web_server_counter = 0
            else:
                web_server_counter = int(web_server_counter)
        else:
            web_server_counter = counter
        return f"Web server counter: {web_server_counter}", 200
    except:
        return "Internal Error, Please check redis connection", 500


@app.route('/', defaults={'user_path': ''}, methods=['GET','POST'])
@app.route('/<path:user_path>', methods=['GET','POST'])
def web_server(user_path):
    """
        catch all routes.
    """
    if request.method == "POST":
        return counter_service_post()
    elif request.method == "GET":
        return counter_service_get()
    

if __name__ == "__main__":
    app.run('0.0.0.0',port=80)
    