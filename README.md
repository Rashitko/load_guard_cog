# Load Guard

The Load Guard is a cog for the Up framework, which adds the ability to monitor the utilization of the system. Load Guard sends the Panic Command if the utilization is higher than a specified threashold.

## Installation ##
Currently **only** installation **from source** is possible.  
Clone the repository <pre>git clone https://github.com/Rashitko/serial_provider_cog.git</pre> and run the following in the root of the cog.<pre>python setup.py install</pre>
After installation run
```bash
up register -n load_guard
```
in root of your application in order to register the Load Guard.

## Usage ##
Load Guard uses the [psutil](https://github.com/giampaolo/psutil) to obtain details about utilization.  
To get the cpu utilization use
```python
load_guard.cpu_utilization #10, which means 10%
```

To get the information about used RAM use
```python
load_guard.ram #30, which means that 30% of virtual memory available is used
```

The default threshold are following:
* if CPU utilization is **>= 80%** panic mode is **entered**
* if CPU utilization is **<= 65%** panic mode is **left**

The default interval for checking the utilization is **0.5s**.  

The thresholds and interval can be set in the generated config file `load_guard.yml` or with the following setters:
```python
load_guard.interval = 0.1             #if the desired interval is 0.1s
load_guard.panic_threshold = 60       #if panic mode should be entered if utilization is >= 60%
load_guard.calm_down_threshold = 20   #if panic mode should be left if utilization is <= 20%
```

See the **Command** section for the details about command sent when panic mode is eneterd/left. Please note that the panic mode is entered/left **based only** on CPU utilization 

## Command ##
The Load Guard defines the **Panic Command**. This command is sent each time the panic mode is entered of left.  

The **command name** is 
```
load_guard.panic
``` 
and it contains the following data:
```
{
  "panic": true|false,  #whether panic mode has been entered or left
  "utilization": 64.5   #utilization when the system enters/leaves the panic mode
}
```

## Telemetry ##
The Load Guard adds the following JSON to the telemetry:
```json
{
  "load": {
    "cpu": 12.5,
    "ram": 25.5
  }
}
```