import numbers
from typing import Callable, Union

import commune
import pandas
import requests
import torch
from substrateinterface import Keypair
from substrateinterface.utils import ss58

U16_MAX = 65535 # 2**16 - 1
U64_MAX = 18446744073709551615 # 2**64 - 1


def strtobool(val: str) -> bool:
    """
    Converts a string to a boolean value.

    truth-y values are 'y', 'yes', 't', 'true', 'on', and '1';
    false-y values are 'n', 'no', 'f', 'false', 'off', and '0'.

    Raises ValueError if 'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

def ss58_address_to_bytes(ss58_address: str) -> bytes:

    """Converts a ss58 address to a bytes object."""
    import scalecodec
    account_id_hex: str = scalecodec.ss58_decode(ss58_address, bittensor.__ss58_format__)
    return bytes.fromhex(account_id_hex)

def u8_key_to_ss58(u8_key: List[int]) -> str:
    
    r"""
    Converts a u8-encoded account key to an ss58 address.

    Args:
        u8_key (List[int]): The u8-encoded account key.
    """
    import scalecodec
    # First byte is length, then 32 bytes of key.
    return scalecodec.ss58_encode( bytes(u8_key).hex(), bittensor.__ss58_format__)

def U16_NORMALIZED_FLOAT( x: int ) -> float:
    return float( x ) / float( U16_MAX ) 

def U64_NORMALIZED_FLOAT( x: int ) -> float:
    return float( x ) / float( U64_MAX )


def indexed_values_to_dataframe ( 
        prefix: Union[str, int],
        index: Union[list, torch.LongTensor], 
        values: Union[list, torch.Tensor],
        filter_zeros: bool = False
    ) -> 'pandas.DataFrame':
    # Type checking.
    if not isinstance(prefix, str) and not isinstance(prefix, numbers.Number):
        raise ValueError('Passed prefix must have type str or Number')
    if isinstance(prefix, numbers.Number):
        prefix = str(prefix)
    if not isinstance(index, list) and not isinstance(index, torch.Tensor):
        raise ValueError('Passed uids must have type list or torch.Tensor')
    if not isinstance(values, list) and not isinstance(values, torch.Tensor):
        raise ValueError('Passed values must have type list or torch.Tensor')
    if not isinstance(index, list):
        index = index.tolist()
    if not isinstance(values, list):
        values = values.tolist()

    index = [ idx_i for idx_i in index if idx_i < len(values) and idx_i >= 0 ]
    dataframe = pandas.DataFrame(columns=[prefix], index = index )
    for idx_i in index:
        value_i = values[ idx_i ]
        if value_i > 0 or not filter_zeros:
            dataframe.loc[idx_i] = pandas.Series( { str(prefix): value_i } )
    return dataframe


def unbiased_topk( values, k, dim=0, sorted = True, largest = True):
    r""" Selects topk as in torch.topk but does not bias lower indices when values are equal.
        Args:
            values: (torch.Tensor)
                Values to index into.
            k: (int):
                Number to take.
            
        Return:
            topk: (torch.Tensor):
                topk k values.
            indices: (torch.LongTensor)
                indices of the topk values.
    """
    permutation = torch.randperm(values.shape[ dim ])
    permuted_values = values[ permutation ]
    topk, indices = torch.topk( permuted_values,  k, dim = dim, sorted=sorted, largest=largest )
    return topk, permutation[ indices ]



def is_valid_ss58_address( address: str ) -> bool:
    """
    Checks if the given address is a valid ss58 address.

    Args:
        address(str): The address to check.

    Returns:
        True if the address is a valid ss58 address for Bittensor, False otherwise.
    """
    try:
        return ss58.is_valid_ss58_address( address, valid_ss58_format=commune.__ss58_format__ )
    except (IndexError):
        return False

def is_valid_ed25519_pubkey( public_key: Union[str, bytes] ) -> bool:
    """
    Checks if the given public_key is a valid ed25519 key.

    Args:
        public_key(Union[str, bytes]): The public_key to check.

    Returns:    
        True if the public_key is a valid ed25519 key, False otherwise.
    
    """
    try:
        if isinstance( public_key, str ):
            if len(public_key) != 64 and len(public_key) != 66:
                raise ValueError( "a public_key should be 64 or 66 characters" )
        elif isinstance( public_key, bytes ):
            if len(public_key) != 32:
                raise ValueError( "a public_key should be 32 bytes" )
        else:
            raise ValueError( "public_key must be a string or bytes" )

        keypair = Keypair(
            public_key=public_key,
            ss58_format=commune.__ss58_format__
        )

        ss58_addr = keypair.ss58_address
        return ss58_addr is not None

    except (ValueError, IndexError):
        return False

def is_valid_address_or_public_key( address: Union[str, bytes] ) -> bool:
    """
    Checks if the given address is a valid destination address.

    Args:
        address(Union[str, bytes]): The address to check.

    Returns:
        True if the address is a valid destination address, False otherwise.
    """
    if isinstance( address, str ):
        # Check if ed25519
        if address.startswith('0x'):
            return is_valid_ed25519_pubkey( address )
        else:
            # Assume ss58 address
            return is_valid_ss58_address( address )
    elif isinstance( address, bytes ):
        # Check if ed25519
        return is_valid_ed25519_pubkey( address )
    else:
        # Invalid address type
        return False

def strtobool_with_default( default: bool ) -> Callable[[str], bool]:
    """
    Creates a strtobool function with a default value.

    Args:
        default(bool): The default value to return if the string is empty.

    Returns:
        The strtobool function with the default value.
    """
    return lambda x: strtobool(x) if x != "" else default


def strtobool(val: str) -> bool:
    """
    Converts a string to a boolean value.

    truth-y values are 'y', 'yes', 't', 'true', 'on', and '1';
    false-y values are 'n', 'no', 'f', 'false', 'off', and '0'.

    Raises ValueError if 'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))



def get_ss58_format( ss58_address: str ) -> int:
    """Returns the ss58 format of the given ss58 address."""
    return ss58.get_ss58_format( ss58_address )

def strtobool_with_default( default: bool ) -> Callable[[str], bool]:
    """
    Creates a strtobool function with a default value.

    Args:
        default(bool): The default value to return if the string is empty.

    Returns:
        The strtobool function with the default value.
    """
    return lambda x: strtobool(x) if x != "" else default