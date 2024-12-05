import json
import os

raw_data = """
1	
Bitcoin
BTC
Bitcoin
$ 95,816	-0.26%	3.28%	38.52%	67.51%	$ 1.90T	$ 115.96B	19.79M
2	
Ethereum
ETH
Ethereum
$ 3,671.22	0.70%	7.99%	48.32%	52.14%	$ 442.16B	$ 50.08B	120.44M
3	
XRP
XRP
XRP
$ 2.55	-6.41%	85.73%	402.36%	360.63%	$ 145.48B	$ 68.05B	57.05B
4	
Tether
USDT
Tether
$ 1.001038	0.04%	0.08%	0.11%	-0.03%	$ 130.85B	$ 405.81B	130.72B
5	
Solana
SOL
Solana
$ 237.61	3.91%	2.41%	45.09%	79.09%	$ 112.88B	$ 17.50B	475.08M
6	
Binance Coin
BNB
Binance Coin
$ 752.77	15.42%	21.74%	33.79%	45.50%	$ 111.09B	$ 9.15B	147.58M
7	
Dogecoin
DOGE
Dogecoin
$ 0.415237	-1.82%	6.37%	172.85%	330.38%	$ 61.04B	$ 17.73B	147.01B
8	
Cardano
ADA
Cardano
$ 1.213284	-5.99%	26.15%	263.85%	277.75%	$ 42.55B	$ 7.97B	35.07B
9	
USD Coin
USDC
USD Coin
$ 0.999958	0.00%	0.00%	0.01%	0.00%	$ 39.01B	$ 11.77B	39.01B
10	
TRON
TRX
TRON
$ 0.405032	78.56%	106.04%	144.97%	170.66%	$ 34.96B	$ 19.49B	86.31B
11	
Avalanche
AVAX
Avalanche
$ 52.26	1.60%	21.63%	119.04%	139.60%	$ 21.39B	$ 3.61B	409.28M
12	
Shiba Inu
SHIB
Shiba Inu
$ 0.00002998	2.63%	22.10%	76.32%	123.22%	$ 17.66B	$ 2.96B	589.26T
13	
Toncoin
TON
Toncoin
$ 6.91	4.51%	11.44%	41.96%	50.82%	$ 17.60B	$ 1.51B	2.55B
14	
Stellar
XLM
Stellar
$ 0.510986	-9.79%	16.97%	457.29%	459.96%	$ 15.37B	$ 6.00B	30.08B
15	
Polkadot
DOT
Polkadot
$ 9.98	-1.04%	23.24%	162.16%	147.55%	$ 15.21B	$ 2.95B	1.52B
16	
Chainlink
LINK
Chainlink
$ 24.07	-0.63%	35.90%	122.67%	135.31%	$ 15.09B	$ 5.07B	626.85M
17	
Wrapped Bitcoin
WBTC
Wrapped Bitcoin
$ 95,598	-0.31%	3.18%	38.43%	67.42%	$ 14.86B	$ 125.35M	155,477
18	
Hedera Hashgraph
HBAR
Hedera Hashgraph
$ 0.328598	-11.89%	143.15%	659.80%	573.04%	$ 11.75B	$ 8.39B	35.75B
19	
Bitcoin Cash
BCH
Bitcoin Cash
$ 572.83	5.91%	15.39%	68.87%	83.81%	$ 11.34B	$ 3.16B	19.80M
20	
Litecoin
LTC
Litecoin
$ 129.67	-1.05%	38.61%	93.36%	98.04%	$ 9.76B	$ 4.17B	75.25M
21	
NEAR Protocol
NEAR
NEAR Protocol
$ 7.39	0.92%	13.22%	99.48%	92.29%	$ 9.00B	$ 2.08B	1.22B
22	
Uniswap
UNI
Uniswap
$ 14.87	5.36%	29.64%	111.28%	133.89%	$ 8.93B	$ 1.94B	600.43M
23	
Pepe Coin
PEPE
Pepe Coin
$ 0.00002048	-0.02%	11.77%	147.96%	182.78%	$ 8.61B	$ 2.42B	420.69T
24	
Sui Crypto
SUI
Sui Crypto
$ 3.68	8.78%	10.50%	93.06%	357.71%	$ 8.61B	$ 6.09B	2.34B
25	
Aptos
APT
Aptos
$ 14.30	2.10%	19.16%	72.41%	139.05%	$ 7.64B	$ 1.91B	534.51M
26	
Internet Computer
ICP
Internet Computer
$ 14.78	5.71%	31.79%	104.48%	98.05%	$ 7.02B	$ 749.41M	474.84M
27	
VeChain
VET
VeChain
$ 0.071938	7.50%	77.04%	261.77%	242.11%	$ 5.83B	$ 2.41B	80.99B
28	
UNUS SED LEO
LEO
UNUS SED LEO
$ 6.03	0.06%	-0.12%	-0.38%	2.55%	$ 5.58B	$ 12.61M	925.35M
29	
Multi-Collateral Dai
DAI
Multi-Collateral Dai
$ 0.999898	-0.01%	-0.17%	-0.10%	-0.19%	$ 5.35B	$ 53.48M	5.35B
30	
Ethereum Classic
ETC
Ethereum Classic
$ 35.51	4.67%	21.87%	99.44%	98.05%	$ 5.32B	$ 2.66B	149.76M
31	
Cronos
CRO
Cronos
$ 0.199977	-0.61%	16.26%	176.25%	155.39%	$ 5.31B	$ 230.98M	26.57B
32	
Fetch.ai
FET
Fetch.ai
$ 1.970198	2.69%	42.36%	71.27%	75.17%	$ 4.97B	$ 1.23B	2.52B
33	
Bittensor
TAO
Bittensor
$ 635.33	3.97%	14.14%	46.61%	151.61%	$ 4.69B	$ 811.54M	7.38M
34	
Filecoin
FIL
Filecoin
$ 7.72	4.45%	41.76%	129.45%	130.38%	$ 4.67B	$ 2.51B	605.35M
35	
Arbitrum
ARB
Arbitrum
$ 1.075352	2.96%	19.06%	120.97%	116.43%	$ 4.41B	$ 1.83B	4.10B
36	
Algorand
ALGO
Algorand
$ 0.523115	-2.22%	75.58%	373.66%	339.38%	$ 4.34B	$ 3.82B	8.29B
37	
Kaspa
KAS
Kaspa
$ 0.164479	4.61%	9.35%	47.20%	6.48%	$ 4.15B	$ 582.32M	25.26B
38	
Polygon Ecosystem Token
POL
Polygon Ecosystem Token
$ 0.713084	3.72%	33.21%	135.88%	88.76%	$ 4.04B	$ 2.06B	5.67B
39	
Stacks
STX
Stacks
$ 2.59	5.82%	23.62%	73.41%	79.08%	$ 3.89B	$ 1.20B	1.50B
40	
Cosmos
ATOM
Cosmos
$ 9.71	-1.45%	22.15%	143.58%	140.09%	$ 3.80B	$ 1.09B	390.93M
41	
Aave
AAVE
Aave
$ 242.28	6.33%	26.83%	81.70%	82.67%	$ 3.63B	$ 1.49B	14.99M
42	
Monero
XMR
Monero
$ 196.79	20.11%	30.67%	30.38%	13.97%	$ 3.63B	$ 519.13M	18.45M
43	
Celestia
TIA
Celestia
$ 8.27	6.74%	0.32%	83.42%	102.96%	$ 3.60B	$ 1.60B	435.82M
44	
OKB
OKB
OKB
$ 59.99	9.66%	13.59%	59.42%	63.45%	$ 3.60B	$ 39.75M	60.00M
45	
Fantom
FTM
Fantom
$ 1.263417	6.24%	12.99%	113.39%	225.92%	$ 3.54B	$ 2.39B	2.80B
46	
Render Token
RENDER
Render Token
$ 8.86	3.46%	18.51%	98.30%	82.31%	$ 3.48B	$ 619.65M	392.46M
47	
Dogwifhat
WIF
Dogwifhat
$ 3.30	4.59%	8.36%	58.38%	109.50%	$ 3.30B	$ 2.52B	998.84M
48	
MANTRA DAO
OM
MANTRA DAO
$ 3.92	10.24%	6.78%	190.82%	318.42%	$ 3.28B	$ 712.14M	837.54M
49	
Injective
INJ
Injective
$ 32.97	2.22%	11.00%	91.51%	92.20%	$ 3.26B	$ 833.54M	98.85M
50	
Optimism
OP
Optimism
$ 2.57	-0.37%	13.34%	82.15%	91.66%	$ 3.23B	$ 1.01B	1.26B
"""

lines = raw_data.strip().split('\n')
result = []

for i in range(0, len(lines), 5):  # Process 5 lines at a time
    try:
        rank = int(lines[i].strip())
        name = lines[i + 1].strip()
        data = lines[i + 4].split('\t')

        if len(data) < 8:
            print(f"Skipping entry due to insufficient data: {lines[i:i + 5]}")
            continue

        market_cap = data[5].replace('$', '').replace(' ', '')
        market_cap_usd = float(market_cap[:-1]) * (1e12 if market_cap[-1] == 'T' else 1e9)

        result.append({
            "name": name,
            "rank": rank,
            "market_cap_usd": market_cap_usd,
            "price_usd": float(data[0].replace('$', '').replace(',', '')),
            
        })
    except (ValueError, IndexError) as e:
        print(f"Error processing entry: {lines[i:i + 5]}")
        print(f"Error details: {str(e)}")

# Specify the directory where you want to save the file.
directory = r'C:\Users\khuwa\Cse_Project'
filename = 'data_12_03_2024.json'

# Create the full path for the file.
file_path = os.path.join(directory, filename)

# Save the result to the specified JSON file.
with open(file_path, 'w') as json_file:
    json.dump(result, json_file, indent=4)

print(f"Data saved to {file_path}")