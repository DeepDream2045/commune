<div align="center">

# **Bittensor** <!-- omit in toc -->
[![Discord Chat](https://img.shields.io/discord/308323056592486420.svg)](https://discord.gg/realbittensor)
[![PyPI version](https://badge.fury.io/py/bittensor.svg)](https://badge.fury.io/py/bittensor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

---

### Internet-scale Neural Networks <!-- omit in toc -->

[Discord](https://discord.gg/realbittensor) • [Network](https://taostats.io/) • [Research](https://drive.google.com/file/d/1VnsobL6lIAAqcA1_Tbm8AYIQscfJV4KU)

</div>

This repository contains Bittensor's Python API, which can be used for the following purposes:

1. Querying the Bittensor network as a client.
2. Running and building Bittensor miners and validators.
3. Pulling network state information.
4. Managing TAO wallets, balances, transfers, etc.

Bittensor is a mining network, similar to Bitcoin, that includes built-in incentives designed to encourage computers to provide access to machine learning models in an efficient and censorship-resistant manner. These models can be queried by users seeking outputs from the network, for instance; generating text, audio, and images, or for extracting numerical representations of these input types. Under the hood, Bittensor’s *economic market*, is facilitated by a blockchain token mechanism, through which producers (***miners***) and the verification of the work done by those miners (***validators***) are rewarded. Miners host, train or otherwise procure machine learning systems into the network as a means of fulfilling the verification problems defined by the validators, like the ability to generate responses from prompts i.e. “What is the capital of Texas?. 

The token based mechanism under which the miners are incentivized ensures that they are constantly driven to make their knowledge output more useful, in terms of speed, intelligence and diversity. The value generated by the network is distributed directly to the individuals producing that value, without intermediarias. Anyone can participate in this endeavour, extract value from the network, and govern Bittensor. The network is open to all participants, and no individual or group has full control over what is learned, who can profit from it, or who can access it.

To learn more about Bittensor, please read our [paper](https://drive.google.com/file/d/1VnsobL6lIAAqcA1_Tbm8AYIQscfJV4KU/view).

# Usage
There are currently three primary ways to interact with Bittensor via this repository:

1. [Developers](#Developers)
    - Those attempting to interact with the Bittensor Network to solve tasks.

2. [Miners](#Miners)
    - Individuals, researchers and developers seeking to contribute value into Bittensor and get paid in mining rewards.

3. [Validators](#Validators)
    - TAO holders who are looking to govern Bittensor directly.

# Install
There are three ways to install Bittensor

1. Through the installer:
```bash
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/opentensor/bittensor/master/scripts/install.sh)"
```
2. With pip:
```bash
$ pip3 install bittensor
```
3. From source:
```bash
$ git clone https://github.com/opentensor/bittensor.git
$ python3 -m pip install -e bittensor/
```
4. Using Conda (recommended for **Apple M1**):
```bash
$ conda env create -f ~/.bittensor/bittensor/scripts/environments/apple_m1_environment.yml
$ conda activate bittensor
```

To test your installation, type:
```bash
$ btcli --help
```
or using python
```python
import bittensor as bt
```

# Wallets 

Wallets are the core ownership and identity technology around which all functions on Bittensor are carried out. Bittensor wallets consists of a coldkey and hotkey where the coldkey may contain many hotkeys, while each hotkey can only belong to a single coldkey. Coldkeys store funds securely, and operate functions such as transfers and staking, while hotkeys are used for all online operations such as signing queries, running miners and validating. 

Wallets can be created in two ways.
1. Using the python-api
```python
import bittensor as bt
wallet = bt.wallet()
wallet.create_new_coldkey()
wallet.create_new_hotkey()
print (wallet)
"Wallet (default, default, ~/.bittensor/wallets/)"
```
2. Or using btcli
```bash
$ btcli new_coldkey
    Enter wallet name (default):      

    IMPORTANT: Store this mnemonic in a secure (preferably offline place), as anyone who has possesion of this mnemonic can use it to regenerate the key and access your tokens. 
    The mnemonic to the new coldkey is:
    **** *** **** **** ***** **** *** **** **** **** ***** *****
    You can use the mnemonic to recreate the key in case it gets lost. The command to use to regenerate the key using this mnemonic is:
    btcli regen_coldkey --mnemonic post maid erode shy captain verify scan shoulder brisk mountain pelican elbow

$ btcli new_hotkey
    Enter wallet name (default): d1
    Enter hotkey name (default): 

    IMPORTANT: Store this mnemonic in a secure (preferably offline place), as anyone who has possesion of this mnemonic can use it to regenerate the key and access your tokens. 
    The mnemonic to the new hotkey is:
    **** *** **** **** ***** **** *** **** **** **** ***** *****
    You can use the mnemonic to recreate the key in case it gets lost. The command to use to regenerate the key using this mnemonic is:
    btcli regen_hotkey --mnemonic total steak hour bird hedgehog trim timber can friend dry worry text
```
In both cases you should be able to view your keys by navigating to ~/.bittensor/wallets or viewed by running ```btcli list```
```bash
$ tree ~/.bittensor/
    .bittensor/                 # Bittensor, root directory.
        wallets/                # The folder containing all bittensor wallets.
            default/            # The name of your wallet, "default"
                coldkey         # You encrypted coldkey.
                coldkeypub.txt  # Your coldkey public address
                hotkeys/        # The folder containing all of your hotkeys.
                    default     # You unencrypeted hotkey information.
```
Your default wallet ```Wallet (default, default, ~/.bittensor/wallets/)``` is always used unless you specify otherwise. Be sure to store your mnemonics safely. If you lose your password to your wallet, or the access to the machine where the wallet is stored, you can always regenerate the coldkey using the mnemonic you saved from above. 
```bash
$ btcli regen_coldkey --mnemonic **** *** **** **** ***** **** *** **** **** **** ***** *****
```

# Developers

Without participating directly in Bittensor’s incentive mechanism, i.e. before holding TAO, becoming a miner, or being a validator, the only way to access Bittensor is by relaying queries through models who have opened exterior access to developers. By default, Bittensor’s api uses the Opentensor Foundation’s endpoint which acts as a bridge onto the network. To access other validators endpoints you must specify their hotkey key, found by running ```btcli list_delegates```
```python
import bittensor as bt

# Query through the foundation endpoint.
print ( bt.prompt( "Heraclitus was a ") )
'Greek philosopher known for his doctrine of change and the famous quote, "No man ever steps in the same river twice."'

# The API also contains BittensorLLM which can be integrated with langchain.
import bittensor as bt
llm = bt.BittensorLLM()
llm( 'prompt me' )

# Return multiple responses for a single prompt.
bt.prompt( "What should I do today?", return_all = True )
[
	'You should buy a boat.',
	'As a language model I cannot answer that question.',
	'You should write in your journal.',
	'Mine bittensor.'
	...
] 

# Specify a separate entrypoint based on the delegate key.
print ( bt.prompt( "Heraclitus was a ", hotkey = "5F4tQyWrhfGVcNhoqeiNsR6KjD4wMZ2kfhLj4oHYuyHbZAc3" ) )
'Greek philosopher known for his doctrine of change and the famous quote, "No man ever steps in the same river twice."'
```

Validators can access Bittensor directly without the need to bridge requests. 
```python
import bittensor as bt
wallet = bt.wallet() # Your validator wallet.
metagraph = bt.metagraph( netuid = 1 ) # Get state from subnetwork 1.
dendrite = bt.text_prompting( keypair = wallet.hotkey, axon = metagraph.axons[ 10 ] ) # Connection to uid 10
dendrite.forward( roles = ['system', 'user'], messages = ['you are my financial advisor', 'should I buy a boat?'] ) 
```

# Miners
The mining challenge on Bittensor is divided into ***subnetworks*** where miners within each subnet are incentivized to contribute distinct forms of value determined by the verification mechanism that that subnetwork’s Validators are running. You can view a list of these subnetworks with ```btcli list_subnets```

```bash
$ btcli list_subnets
    NETUID  NEURONS  MAX_N   DIFFICULTY  TEMPO  CON_REQ  EMISSION  BURN(τ)
    1       691    1.02 K   198.08 T    99     None     28.44%   τ4.75710
    3      4096    4.10 K   320.81 T    99     None     71.56%   τ1.00000
    2      5120
    
    Description:
    	# NETUID: A unique network index on Bittensor
    	# NEURONS: The number of uid slots taken by miners
    	# MAX_N: The total allowed slots on a subnetwork
	# DIFFICULTY: The difficulty of the POW registration challenge required to win a slot.
	# TEMPO: The number of blocks before new tokens are distributed.
	# CON_REQ: The list of subnetworks that a miner must enter before entering this network.
	# EMISSION: The proportion of the total token emission which flows through this network.
	# BURN: The recycle burn cost to enter this network.
```

Each subnetwork contains a set of UIDs, or slots, into which miners must ***register*** into before they are considered for evaluation by validators in the network and thus mine TAO. These slots fill up through continuous registrations and miners are dropped from the network based on performance. Each time a new hotkey is registered to the subnet, the lowest ranked miner is removed from the subnet. The process of registering a miner is competitive, and uses two mutually adaptive method to determine the price to entry, those are:

1. Proof of work based registration. 
```bash
$ btcli register --netuid <subnetwork uid>
```
NOTE: It is suggested that you use a Nvidia GPU to register. To do this, you can install Cubit to enable registrations via your GPU for a faster hash rate.
```bash
(optional): pip install git+https://github.com/opentensor/cubit.git@v1.1.2
```

2. and TAO recycling registration
```bash
$ btcli recycle_register --netuid <subnetwork uid>
```
POW registration is recommmended for miners contributing raw compute power to bittensor and are seeking a method attaining a slot without the token initially. Recycle registration is recommended for anyone seeking to attain slots and already has a small amount of TAO at their disposal. In both cases, the registration requires a ```--netuid``` parameter which specifies which subnetwork the miner is entering. Once they registered the miner attains a slot specified by their UID, this UID is thiers to mine under. To view your slot after registration, run the overview command

```bash
$ btcli overview --netuid <subnetwork uid>
```

Registered miners are free to select from variety of pre-written miners or to write their own using the python api. You can find these miners by cloning this repository locally.
```bash
$ git clone https://github.com/opentensor/bittensor.git
    bittensor/                              # This repo.
        neurons/                            # Miners and Validators across all subnetworks.
            text_prompting/                 # Miners and Validators for the text_prompting subnetwork.
                miners/                     # Miners.
                    GPT4ALL/                # The root folder for the GPT4ALL miner.
                        neuron.py           # GPT4ALL miner main script.
                        requirements.txt     # GPT4ALL requirements.
                        README.md           # GPT4ALL instructions.
                    ...
```
For instance, you can run the GPT4ALL miner on subnetwork 1 as follows. Note: it is recommended to run most miners on machines with a GPU. In the future bittensor/neurons is likely to expand into its own repository. 
```bash
$ python3 -m pip install -r bittensor/neurons/text_prompting/miners/GPT4ALL/requirements.txt
$ python3 bittensor/neurons/text_prompting/miners/GPT4ALL/neuron.py --netuid 1
```

# Validators
Network Validation is open to participants who hold TAO. The validation mechanims uses a dual proof-of-stake, proof-of-work mechanism called Yuma Consensus which you can read about [here](https://drive.google.com/file/d/1VnsobL6lIAAqcA1_Tbm8AYIQscfJV4KU/view). Yuma consensus rewards the agreement between the evaluations of miner-value produced by validators across each subnetwork. Because each subnetwork task is distinct this requires a separate implementation of the each validator for each network. 

Before becoming a validator you will need to register a slot as described above in the mining section. Keys are automatically considered Validators in each subnetwork if the registered hotkey is a member of the top 128 keys ranked by total stake. Stake determines the weight given to the value estimations of your validator in Yuma Consensus. There are exclusively two ways to attain stake on your validator.

1. By staking the funds yourself
```bash
$ btcli stake --help # To add funds to the staking account associated with your wallet.
```

2. Or by attracting delegated stake
```bash
$ btcli nominate --help # to become a key available for delegated stake
$ btcli delegate --help # for others to delegate stake to your wallet.
```
Bittensor's API is designed to allow Validators to write their own validation mechanisms and express their own subjective prefrences about what the network should learn. However, going too far outside consensus reduces the rewards validators attain while performing validation. To ensure your validator remains in alignment with others this repository contains a "core" validator for each subnetwork
```bash
$ tree bittensor/neurons
    bittensor/
        neurons/
            text_to_embedding/
            text_prompting/
                validators/
                    core/
                        neuron.py
```
For instance you can run the core text prompting validator on subnetwork 1 as follows. Note it is also recommended that you run validators on machines with a GPU. In the future bittensor/neurons/valdidators is likely to expand into its own repository. 

# Using the CLI

The Bittensor command line interface (btcli) comes installed with this repository. It is the primary command line tool to deploy, analyze, and interface with the Bittensor network. It can be used to transfer tao, stake, unstake, nominate, delegate, and more. You can use btcli --help command as follows to see a full list of commands
```bash
$ btcli --help
        help                Displays the help.
        list                List wallets.
        stake               Stake to your hotkey accounts.
        update              Updates your bittensor installation.
        inspect             Inspect a wallet cold, hot pair
        weights             Show the weights from chain.
        unstake             Unstake from hotkey accounts.
        overview            Show registered account overview.
        register            Register a wallet to a network.
        transfer            Transfer Tao between accounts.
        nominate            Become a delegate on the network
        new_hotkey          Creates a new hotkey for running a miner under the specified path.
        metagraph           Show the network graph.
        new_coldkey         Creates a new coldkey  for containing balance under the specified path.
        my_delegates        Show all delegates where I am delegating a positive amount of stake.
        list_subnets        List all subnets on the network.
        regen_hotkey        Regenerates a hotkey from a passed mnemonic.
        regen_coldkey       Regenerates a coldkey from a passed value.
        delegate            Delegate Stake to an account.
        undelegate          Undelegate Stake from an account.
        list_delegates      List all delegates on the network.
        regen_coldkeypub    Regenerates a public coldkey from the public part of the coldkey.
        recycle_register    Register a wallet to a network.

    optional arguments:
    -h, 
    --help                  Show this help message and exit
    --config CONFIG         If set, defaults are overridden by passed file.
    --strict                If flagged, config will check that only exact arguemnts have been set.
```

# The Bittensor Package
The bittensor package contains data structures for interacting with the bittensor ecosystem, writing miners, validators and querying the network. Additionally, it provides many utilities for efficient serialization of Tensors over the wire, performing data analysis of the network, and other useful utilities.

Wallet: Interface over locally stored bittensor hot + coldkey styled wallets. 
```python
import bittensor as bt
# Bittensor's wallet maintenance class.
wallet = bt.wallet() 
# Access the hotkey
wallet.hotkey 
# Access the coldkey
wallet.coldkey ( requires decryption )
# Sign data with the keypair.
wallet.coldkey.sign( data )

```

Subtensor: Interfaces with bittensor's blochain and can perform operations like extracting state information or sending transactions.
```python
import bittensor as bt
# Bittensor's chain interface.
subtensor = bt.subtensor() 
# Get the chain block
subtensor.get_current_block()
# Transfer Tao to a destination address.
subtensor.transfer( wallet = wallet, dest = "xxxxxxx..xxxxx", amount = 10.0)
# Register a wallet onto a subnetwork
subtensor.register( wallet = wallet, netuid = 1 )
```

Metagraph: Encapsulates the chain state of a particular subnetwork at a specific block.
```python
import bittensor as bt
# Bittensor's chain state object.
metagraph = bt.metagraph( netuid = 1 ) 
# Resync the graph with the most recent chain state
metagraph.sync()
# Get the list of stake values
print ( metagraph.S )
# Get endpoint information for the entire subnetwork
print ( metagraph.axons )
# Get the hotkey information for the miner in the 10th slot
print ( metagraph.hotkeys[ 10 ] )
# Sync the metagraph at another block
metagraph.sync( block = 100000 )
# Save the metagraph
metagraph.save()
# Load the same
metagraph.load()
```

Axon: Maintains a queryable endpoint for accepting messages on the wire.
```python
import bittensor as bt
# Instantiate a Bittensor endpoint.
axon = bt.axon( wallet = wallet, metagraph = metagraph ) 
# Start servicing messages on the wire.
axon.start()
# Register this axon on a subnetwork
subtensor.serve_axon( netuid = 1, axon = axon )
# Turn off the axon.
axon.stop()
```

Synapse: Implements the wire protocol required to service requests from validators on a subnetwor
```python
import bittensor as bt

# Netuid 1 specification.
class Synapse( bittensor.TextPromptingSynapse ):
   	
	# Return the priority of the request, larger numbers are serviced by the endpoint first.
    	def priority(self, forward_call: "bittensor.TextPromptingForwardCall") -> float: return 0.0
	
	# Return True if the request will not be serviced by this miner endpoint.
    	def blacklist(self, forward_call: "bittensor.TextPromptingForwardCall") -> Union[ Tuple[bool, str], bool ]: return False
	
	# Accept and optionally apply the feedback from a validator on the network.
    	def backward( self, messages: List[Dict[str, str]], response: str, rewards: torch.FloatTensor ) -> str: pass
	
	# Return an output which will be rewarded highly by validators on this subnetwork.
    	def forward(self, messages: List[Dict[str, str]]) -> str: return "hello im a chat bot."
	
# Attach this synapse to the running axon.
synapse = Synapse( axon = axon )
```

Dendrite: Packages and sends messages to synapses over the wire. 
```python
import bittensor as bt
# Connect to the axon running on slot 10, use the wallet to sign messages.
dendrite = bt.text_prompting( keypair = wallet.hotkey, axon = metagraph.axons[10] ) 
# Send a prompt to this endpoint
dendrite.forward( roles = ['user'], messages = ['what are you?'] )
```

## Release
The release manager should follow the instructions of the [RELEASE_GUIDELINES.md](./RELEASE_GUIDELINES.md) document.

## License
The MIT License (MIT)
Copyright © 2021 Yuma Rao

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Acknowledgments
**learning-at-home/hivemind**