"""
    A petition that has encrypted YES|NO signatures but that does not do:

    1) Checking the validity of the petition signatories (are they allowed to sign)
    2) Maintining privacy (the public key of the signatory is used to prevent double signing)

    This petition is an intermediate step towards a full coconut based private petition

"""

####################################################################
# imports
####################################################################
# general
from hashlib import sha256
from json    import dumps, loads, dump
from os.path import join

import subprocess

# chainspace
from chainspacecontract import ChainspaceContract

## contract name
contract = ChainspaceContract('zenroom_petition')

ZENROOM_PATH = "zenroom"
SCRIPT_PATH = "/opt/contracts/"
DATA_PATH = "/tmp/data.json"


def execute_zenroom(script_filename, data_filename = None, key_filename = None):
    commands = [ZENROOM_PATH]
    if data_filename:
        commands = commands + ['-a', data_filename]

    if key_filename:
        commands = commands + ['-k', key_filename]

    commands.append(join(SCRIPT_PATH, script_filename))
    return subprocess.check_output(commands)


def write_data(data, filename=DATA_PATH):
    with open(filename, 'w') as outfile:
        dump(data, outfile)

####################################################################
# methods
####################################################################
# ------------------------------------------------------------------
# init
# ------------------------------------------------------------------
@contract.method('init')
def init():
    # return
    return {
        'outputs': (dumps({'type' : 'PetitionEncToken'}),)
    }

# ------------------------------------------------------------------
# create petition event
# NOTE:
#   - only 'inputs', 'reference_inputs' and 'parameters' are used to the framework
#   - if there are more than 3 param, the checker has to be implemented by hand
# ------------------------------------------------------------------
@contract.method('create_petition')
def create_petition(inputs, reference_inputs, parameters, options, private_filepath):

    data = {
        'options': options
    }

    write_data(data)

    output = loads(execute_zenroom('init.lua', DATA_PATH, private_filepath))

    # new petition object
    new_petition = {
        'type'          : 'PetitionEncObject',
        'options'       : output["options"],
        'scores'        : output["scores"],
        'public'        : output["public"],
        'proves'        : output["proves"]
    }

    # return
    return {
        'outputs': (inputs[0], dumps(new_petition))
    }

# ------------------------------------------------------------------
# add signature
# NOTE:
#   - only 'inputs', 'reference_inputs' and 'parameters' are used to the framework
#   - if there are more than 3 param, the checker has to be implemented by hand
# ------------------------------------------------------------------
@contract.method('add_signature')
def add_signature(inputs, reference_inputs, parameters, option):

    last_signature = loads(inputs[0])
    last_signature['option'] = option

    write_data(last_signature)

    output = loads(execute_zenroom("vote.lua", DATA_PATH))

    new_signature = {
        "public"   : output["public"],
        "options"  : output["options"],
        "scores"   : output["scores"],
        'type'     : 'PetitionEncObject',
    }

    enc_added_signatures = output['increment']
    proof_bin = output['provebin']
    proof_sum = output['prove_sum_one']

    return {
        'outputs': (dumps(new_signature),),
        'extra_parameters' : (
            dumps(enc_added_signatures),
            dumps(proof_bin),
            dumps(proof_sum)
        )
    }

# ------------------------------------------------------------------
# tally
# NOTE:
#   - only 'inputs', 'reference_inputs' and 'parameters' are used to the framework
#   - if there are more than 3 param, the checker has to be implemented by hand
# ------------------------------------------------------------------
@contract.method('tally')
def tally(inputs, reference_inputs, parameters, key_filename):

    # retrieve last petition
    petition = loads(inputs[0])

    write_data(petition)

    output = loads(execute_zenroom('tally.lua', DATA_PATH, key_filename))

    outcome = output['outcome']
    proof = output['proof']

    # pack result
    result = {
        'type'      : 'PetitionEncResult',
        'outcome'   : outcome
    }

    # return
    return {
        'outputs': (dumps(result),),
        'extra_parameters' : (dumps({
            'proof': proof
        }),)
    }

#
# ####################################################################
# # checkers
# ####################################################################
# # ------------------------------------------------------------------
# # check petitions's creation
# # ------------------------------------------------------------------
@contract.checker('create_petition')
def create_petition_checker(inputs, reference_inputs, parameters, outputs, returns, dependencies):
    try:
        # retrieve petition
        petition  = loads(outputs[1])

        write_data(petition)

        output = loads(execute_zenroom('verify_init.lua', DATA_PATH))

        return output["ok"]

    except (KeyError, Exception):
        return False

# ------------------------------------------------------------------
# check add signature
# ------------------------------------------------------------------
@contract.checker('add_signature')
def add_signature_checker(inputs, reference_inputs, parameters, outputs, returns, dependencies):
    try:

        print "CHECKING - parameters " + str(parameters)

        # retrieve petition
        old_signature = loads(inputs[0])
        new_signature = loads(outputs[0])
        num_options = len(old_signature['options'])

        # check format
        if len(inputs) != 1 or len(reference_inputs) != 0 or len(outputs) != 1 or len(returns) != 0:
            return False
        if num_options != len(new_signature['scores']):
            return False
        if old_signature['public'] != new_signature['public']:
            return False

        print "CHECKING - tokens"
        if new_signature['type'] != 'PetitionEncObject':
            return False


        print "CHECKING - Generate params"


        # generate params, retrieve tally's public key and the parameters
        added_signature = loads(parameters[0])
        proof_bin  = loads(parameters[1])
        proof_sum  = loads(parameters[2])

        data = new_signature
        data['prove_sum_one'] = proof_sum
        data['provebin'] = proof_bin
        data['increment'] = added_signature

        write_data(data)

        output = loads(execute_zenroom('verify_vote.lua', DATA_PATH))

        # otherwise
        return output["ok"]

    except (KeyError, Exception):
        return False

# ------------------------------------------------------------------
# check tally
# ------------------------------------------------------------------
@contract.checker('tally')
def tally_checker(inputs, reference_inputs, parameters, outputs, returns, dependencies):
    try:

        # retrieve petition
        petition   = loads(inputs[0])
        result = loads(outputs[0])

        # check format
        if len(inputs) != 1 or len(reference_inputs) != 0 or len(outputs) != 1 or len(returns) != 0:
            return False
        if len(petition['options']) != len(result['outcome']):
            return False

        # check tokens
        if result['type'] != 'PetitionEncResult':
            return False

        data = loads(parameters[0])
        result['proof'] = data['proof']
        result['scores'] = petition['scores']
        result['public'] = petition['public']

        write_data(result)

        output = loads(execute_zenroom('verify_tally.lua', DATA_PATH))

        # otherwise
        return output['ok']

    except (KeyError, Exception):
        return False


####################################################################
# main
####################################################################
if __name__ == '__main__':
    contract.run()



####################################################################
