"""An example smart contract to demonstrate three layer deep cross-contract
calls."""

from chainspacecontract import ChainspaceContract
from chainspacecontract.examples.increment_twice import contract as increment_twice_contract

contract = ChainspaceContract('increment_thrice')
contract.register_dependency(increment_twice_contract)


@contract.method('init')
def init():
    return {
        'outputs': (0,)
    }


@contract.method('increment')
def increment(inputs, reference_inputs, parameters):
    integer = int(inputs[0])
    increment_twice_contract.increment((parameters[1],), None, (parameters[0],))
    return {
        'outputs': (str(integer + 1),)
    }

if __name__ == '__main__':
    contract.run()
