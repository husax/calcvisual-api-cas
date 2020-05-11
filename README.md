# calcvisual-api-cas

```
docker build -t calcvisual-api-cas:latest .
```
```
docker run -d -p 5000:5000 calcvisual-api-cas:latest
```
http://127.0.0.1:5000/


docker stop $(docker ps -a -q)
docker system prune -a


## References
* https://flask-cors.readthedocs.io/en/latest/
* https://medium.com/@doedotdev/docker-flask-a-simple-tutorial-bbcb2f4110b5
* https://www.geeksforgeeks.org/python-sympy-diff-method/