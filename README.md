# ethcloud

[<img src="https://img.shields.io/pypi/v/ethcloud.svg">](https://pypi.python.org/pypi/ethcloud)
[<img src="https://img.shields.io/pypi/l/ethcloud.svg">](https://pypi.python.org/pypi/ethcloud)
[<img src="https://img.shields.io/pypi/pyversions/ethcloud.svg">](https://pypi.python.org/pypi/ethcloud)
[<img src="https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg">](https://saythanks.io/to/kgritesh)


 A cli tool to launch, use and manange an ethereum client on the cloud. Under the 
 hood `ethcloud` uses [ansible](https://www.ansible.com/) and  native cloud provider api's 
 to launch a new cloud instance, runs an ethereum client on it and provide an 
 interface as if the client is running locally. It tries to support all commands
 and options for the ethereum client tool and comes with good defaults, but allows configuring
  all the parameters with a configuration file. 

# Installation

    $ pip install ethcloud


# Under the hood

`ethcloud` uses ansible and ssh under the hood to launch a new instance and perform 
  basic server hardening tasks to ensure security for the node. It consists of following
  steps
  
  - Use ansible modules to interact with cloud providers and provision a new instance 
  in the user's account. Currently we only support `aws` and `ubuntu` instances
  but should be very easy to extend to other cloud providers and platform. 
  
  - Install some basic packages like vim, curl, wget using platform's package maanger
  
  - Update kernel parameters required for security
  
  - Add any default users that needs to be setup on the cloud instance
  
  - Add fail2ban service to monitor logs and protect against brute force ssh
  attacks
  
  - Add ufw firewall to only allow ports required by the ethereum client and ssh
  
  - Update the hostname for the instance to the desired name for the instance
  
  - Install the ethereum client and create a `systemd service` for it so that its
   managed by the OS
   
  - Currently for `aws`, we also forward the logs from `systemd journal` to 
    cloudwatch service for easy log monitoring
    
  - Finally create a ssh tunnel from a local port to the JSON RPC 
  port of the remote ethereum client. This ensures that you you can use the 
   remote node as local 
     
     

# Usage    
    Usage: ethcloud [OPTIONS] COMMAND [ARGS]...
    
      A tool to launch and interface with a ethereum client running on a remote
      instance
    
    Options:
      --version  Show the version and exit.
      --help     Show this message and exit.
    
    Commands:
      account
      attach   Attach to geth console.
      delete   Delet an existing cloud instance running...
      export   Export the blockchain into a file
      launch   Launch a new instance in the cloud and start...
      logs     Show ethereum client logs
      start    Restart Ethereum Client with updated config
      stop     Stop geth ethereum client without destroying...
      update   Update an existing cloud instance running...

All commands require a config file which describes the cloud provider, unique instance name
 , the ethereum clientto be used, and other configuration required by the cloud provider
   and ethereum client
   
   
## Coniguration

Default configuration file is 

    provider: aws  # Provider to be used [Required]
    instance_name: ethereum-node-1 # Unique identifier for the instance [Required]
    ethereum_client: geth
    config: # Cloud Provider specific configureation
        remote_user: 'ubuntu' # User to be used to login [Required]
        aws_region: 'ap-south-1' # AWS Region [Required]    
        ec2_instance_type: 't2.small' # AWS Instance type [Required]    
        aws_key: '' # AWS Key to be used as default user ssh public key 

There are other optional configuration which can be used. Other configuration can
 be found at 'ethcloud/provision/vars/'
          
## Commands

Each of these commands takes the config file as a required option. Also each of these 
commands takes additional options which are directly passed to the underlying ethereum 
client command

### launch 

    Usage: ethcloud launch [OPTIONS]
    
      Launch a new instance in the cloud and start a ethereum client on the
      instance. 
    
    Options:
      -c, --cloud-config PATH  Path to the cloud config to use to launch
                               [required]
      -v, --verbose            verbose mode or level (support upto 4 levels)
      -q, --quiet              Only log errors and warnings
      --help                   Show this message and exit.


Any extra option is as it is used while starting the specified ethereum client.

For eg

    ethcloud launch -c .ethconfig --rinkeby --rpc 
    
This command will launch a new cloud instance, start a geth client on rinkeby network
with rpc enabled

### logs

    Usage: ethcloud logs [OPTIONS]
    
      Show ethereum client logs
    
    Options:
      -c, --cloud-config PATH  Path to the cloud config to use to launch
                               [required]
      --help                   Show this message and exit.

### attach
 
     Usage: ethcloud attach [OPTIONS]
     
       Attach to ethereum client console.
     
     Options:
       -c, --cloud-config PATH  Path to the cloud config to use to launch
                                [required]
       --help                   Show this message and exit.



### start
    
    Usage: ethcloud start [OPTIONS]
    
      Restart Ethereum Client with updated config
    
    Options:
      -c, --cloud-config PATH  Path to the cloud config to use to launch
                               [required]
      --help                   Show this message and exit.
      

### stop

    Usage: ethcloud stop [OPTIONS]
    
      Stop geth ethereum client without destroying the instance
    
    Options:
      -c, --cloud-config PATH  Path to the cloud config to use to launch
                               [required]
      --help                   Show this message and exit.

      
### account
      
    Usage: ethcloud account [OPTIONS] COMMAND [ARGS]...
    
      Manage accounts, list all existing accounts, import a private key into a
      new account, create a new account or update an existing account.
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      import  Imports an unencrypted private key from...
      list    List existing accounts
      new     Create a new account
      update  Update account password      
      
### export

    Usage: ethcloud export [OPTIONS] FILEPATH [FIRST_BLOCK] [LAST_BLOCK]
    
      Export the blockchain into a file
    
    Options:
      -c, --cloud-config PATH  Path to the cloud config to use to launch
                               [required]
      --help                   Show this message and exit.


## Major TO DO'S

- Support more cloud providers apart from aws ec2. For eg: linode/digital ocean/
google cloud platform / azure etc

- Support more ethereum clients apart from geth like parity and cpp-ethereum

- Support more platforms apart from ubuntu.

- Show ethereum client specific extra options in help depending upon the ethereum client
   being used
   
- Better Documentation

- Tests


## Contributing

#### Feature Requests

I'm always looking for suggestions to improve this project. If you have a
suggestion for improving an existing feature, or would like to suggest a
completely new feature, please file an issue with my
[Github repository](https://github.com/loanzen/falcon-auth/issues>)

#### Bug Reports

You may file bug reports on [Github Issues](https://github.com/loanzen/falcon-auth/issues>)

#### Pull Requests

Along with my desire to hear your feedback and suggestions,
I'm also interested in accepting direct assistance in the form of new code or documentation.
Please feel free to file pull requests.
