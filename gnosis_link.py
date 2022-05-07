from unittest import result
import requests


def website_link(safe_address, safeTxHash, network='eth'):
    return f"Please try again at https://gnosis-safe.io/app/{network}:{safe_address}/transactions/multisig_{safe_address}_{safeTxHash}"


def check_safe_status(safe_address, network='eth'):
    result_list = []

    networks = {
        "eth": "https://safe-transaction.gnosis.io/api/v1/safes/{safe_address}/multisig-transactions/?limit=10",
        "polygon": "https://safe-transaction.polygon.gnosis.io/api/v1/safes/{safe_address}/multisig-transactions/?limit=10",
        "others": "https://safe-transaction.{network}.gnosis.io/api/v1/safes/{safe_address}/multisig-transactions/?limit=10"
    }

    if network in networks:
        x = requests.get(networks[network].format(safe_address=safe_address))
    else:
        x = requests.get(networks["others"].format(safe_address=safe_address))

    response = x.json()
    trx_list = {}
    for i in response['results']:
        nonce_tup = ()
        if i['isSuccessful'] == None:
            if i['nonce'] not in trx_list:
                trx_list[i['nonce']] = i['safeTxHash']
                nonce_tup = (f"Nonce {i['nonce']} is not yet executed ", website_link(
                    safe_address, i['safeTxHash'], network))
            else:
                nonce_tup = f"Nonce {i['nonce']} is already in the list"
        elif i['isSuccessful'] == True:
            trx_list[i['nonce']] = i['safeTxHash']
            nonce_tup = f"Nonce {i['nonce']} was executed Successfully"
        else:
            trx_list[i['nonce']] = i['safeTxHash']
            nonce_tup = (f"Nonce {i['nonce']} has Failed ", website_link(
                safe_address, i['safeTxHash'], network))
        result_list.append(nonce_tup)
    return result_list


if __name__ == "__main__":
    safe_address = '0xd605bB8A3DA1f7f777276D3c97c828aAc3Dd4252'
    network = 'eth'
    results = check_safe_status(safe_address, network)
    for i in results:
        print(i)
