# PI-Bridge
Backend Service for [lumap project](https://github.com/zachzhu2016/lumap). 

# Daemon
Daemon is a Node.js module running on localhost for getting acccess tokens from Bentley Systems' iTwin backend service. 

# main.py 
A Flask app used to respond to requests from https://www.lehighmap.com. It's responsible for serving Bentley account access tokens, caching certain PI data, and relaying requests to PI Web API. 
