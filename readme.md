Resultado aqui:
```text
/home/marcos/.virtualenvs/exploring_paralelism/bin/python /home/marcos/work/storm/labs/exploring_paralelism/main.py 
Starting singlethread
Singlethread texts: #89 in National Universities (tie), (tie), (tie), 12,000, 2.1.1, 2.1.2, 2.1.3, 346 VISUALIZAÇÕES...
singlethread took 6.912031650543213 seconds
Starting multithread
Using 20 workers
Multithread texts: 12,000, 1867 - present, 2.1.1, 2.1.2, 2.1.3, 346 VISUALIZAÇÕES, 43 línguas, 53 nations., 53 states...
multithread took 2.4511075019836426 seconds
Starting multiproc
Using 20 processes
Multiprocess texts: #89 in National Universities (tie), (tie), (tie), 12,000, 2.1.1, 2.1.2, 2.1.3, 346 VISUALIZAÇÕES,...
multiproc took 2.3061654567718506 seconds

Process finished with exit code 0
```
O multithread está bem próximo do multiprocess. (provável característica do requests.get)
