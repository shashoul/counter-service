 
# counter-service
    flask app counts the amount of POST
    requests and return it on every GET request.
    The service can be run in two mode with redis (we should provide redis_host)
    and without redis( we using global variable and the data is just kept in memory ,
    and will be lost once the app is down or crashing.)


# To build the application you should be in the folder contains the Dockerfile:

    docker build -t counter-service .

# Environment Variables

        1. redis_host (default is "")
        2. redis_port (default is 6379)

        docker run -d -p 80:80 \
            -e redis_host="" \        #redis host name.(default is "")
            -e redis_port=6379        #redis port number.(default is 6379)   


# To run the application without redis:
    
    docker run -d -p 80:80 --name counter-service counter-service


# To run the application with redis:
  
    to launch a redis 
     docker run -d --name my-redis -p 6379:6379 redis

  
    docker run -d -p 80:80 \             
        --link my-redis \               #link to the redis docker that running.
        -e redis_host=my-redis \        #provide the app redis host.
        --name counter-service \
         counter-service
    


