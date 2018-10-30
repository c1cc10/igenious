# igenius
Backend remote exercise

Easy and simple docker server POC application. To deploy it using docker:
* download this repository 
* into the repository directory, build it by command: _docker build -t igenius ._
* once previous command has been completed, run it: _docker run -p 8888:8888 igenius_


Server will be listening on port 8888. 
You can run basic tests by using file _test.py_ on another command line console. 
Just type _python3 test.py_. 
Warning: _test.py_ needs python 3.6 and urllib to run.

Side note: docker isn't mandatory. 
This service can be run by simply launching _python3 xchange.py_ but it needs python3.6, tornado and urllib3 installed before you have a go.
