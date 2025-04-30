import json
import os
import re

raw_data = """
1	
Bitcoin
BTC
Bitcoin
$ 83,452	1.02%	-5.31%	-1.78%	-12.24%	$ 1.66T	$ 44.36B	19.83M
2	
Ethereum
ETH
Ethereum
$ 1,842.54	1.74%	-11.53%	-15.59%	-45.93%	$ 222.21B	$ 20.17B	120.60M
3	
Tether
USDT
Tether
$ 1.000406	-0.02%	-0.02%	-0.09%	0.07%	$ 144.00B	$ 102.34B	143.94B
4	
XRP
XRP
XRP
$ 2.12	-0.96%	-13.91%	-1.62%	0.05%	$ 122.85B	$ 9.08B	57.95B
5	
Binance Coin
BNB
Binance Coin
$ 604.83	0.44%	-4.58%	-0.08%	-14.90%	$ 89.26B	$ 1.79B	147.58M
6	
Solana
SOL
Solana
$ 126.70	1.03%	-11.17%	-9.89%	-36.07%	$ 64.45B	$ 7.57B	508.71M
7	
USD Coin
USDC
USD Coin
$ 0.999908	0.00%	0.01%	0.01%	0.00%	$ 60.08B	$ 12.09B	60.08B
8	
Dogecoin
DOGE
Dogecoin
$ 0.167434	-0.51%	-8.19%	-17.59%	-48.63%	$ 24.83B	$ 2.93B	148.33B
9	
Cardano
ADA
Cardano
$ 0.658985	-1.38%	-9.87%	3.69%	-24.24%	$ 23.21B	$ 1.64B	35.22B
10	
TRON
TRX
TRON
$ 0.237761	2.91%	3.44%	2.69%	-7.28%	$ 20.46B	$ 1.03B	86.05B
11	
Toncoin
TON
Toncoin
$ 4.07	8.13%	10.13%	26.13%	-26.87%	$ 10.08B	$ 939.84M	2.48B
12	
Chainlink
LINK
Chainlink
$ 13.59	0.05%	-10.00%	-6.40%	-34.43%	$ 8.67B	$ 726.92M	638.10M
13	
UNUS SED LEO
LEO
UNUS SED LEO
$ 9.15	-5.23%	-6.12%	-6.20%	4.22%	$ 8.46B	$ 1.35M	924.38M
14	
Stellar
XLM
Stellar
$ 0.267673	0.16%	-7.65%	-10.15%	-21.30%	$ 8.22B	$ 262.36M	30.71B
15	
Avalanche
AVAX
Avalanche
$ 18.95	-1.77%	-11.57%	-11.40%	-48.40%	$ 7.85B	$ 596.43M	414.19M
16	
Shiba Inu
SHIB
Shiba Inu
$ 0.00001249	-0.24%	-7.59%	-8.28%	-42.32%	$ 7.36B	$ 233.52M	589.25T
17	
Litecoin
LTC
Litecoin
$ 83.37	-3.36%	-11.21%	-33.58%	-20.05%	$ 6.30B	$ 1.19B	75.56M
18	
Polkadot
DOT
Polkadot
$ 4.04	-0.97%	-14.16%	-12.08%	-40.85%	$ 6.28B	$ 428.29M	1.56B
19	
MANTRA DAO
OM
MANTRA DAO
$ 6.26	0.19%	-8.38%	-16.05%	59.85%	$ 6.09B	$ 92.10M	973.22M
20	
Bitcoin Cash
BCH
Bitcoin Cash
$ 304.75	0.44%	-8.51%	-1.78%	-32.17%	$ 6.05B	$ 591.40M	19.84M
21	
Hedera Hashgraph
HBAR
Hedera Hashgraph
$ 0.164916	-2.86%	-14.13%	-29.89%	-40.30%	$ 5.90B	$ 435.07M	35.75B
22	
Bitget Token
BGB
Bitget Token
$ 4.51	-1.70%	-6.93%	11.96%	-23.97%	$ 5.41B	$ 247.49M	1.20B
23	
Ethena USDe
USDE
Ethena USDe
$ 1.000759	0.02%	0.06%	0.07%	0.22%	$ 5.41B	$ 78.52M	5.40B
24	
Sui Crypto
SUI
Sui Crypto
$ 2.29	-2.67%	-5.53%	-18.36%	-46.13%	$ 5.36B	$ 2.10B	2.34B
25	
Multi-Collateral Dai
DAI
Multi-Collateral Dai
$ 0.99979	0.00%	-0.12%	-0.06%	-0.26%	$ 5.35B	$ 159.87M	5.35B
26	
USDS
USDS
USDS
$ 0.999993	0.15%	0.29%	-0.14%	-0.34%	$ 5.26B	$ 236,941	5.26B
27	
Pi Network
PI
Pi Network
$ 0.724436	-5.92%	-22.65%	-62.90%		$ 4.91B	$ 449.72M	6.77B
28	
Hyperliquid
HYPE
Hyperliquid
$ 13.21	4.82%	-21.79%	-31.65%	-49.39%	$ 4.41B	$ 33.91M	333.93M
29	
Monero
XMR
Monero
$ 215.50	-0.57%	-2.32%	-1.32%	10.85%	$ 3.98B	$ 82.11M	18.45M
30	
Uniswap
UNI
Uniswap
$ 6.00	1.02%	-14.40%	-18.35%	-55.72%	$ 3.60B	$ 191.00M	600.59M
31	
Aptos
APT
Aptos
$ 5.37	0.80%	-8.36%	-16.09%	-39.77%	$ 3.17B	$ 245.29M	589.92M
32	
NEAR Protocol
NEAR
NEAR Protocol
$ 2.61	-1.28%	-11.75%	-17.26%	-48.87%	$ 3.10B	$ 377.00M	1.19B
33	
Pepe Coin
PEPE
Pepe Coin
$ 0.0₅7238	3.27%	-8.67%	-3.09%	-65.77%	$ 3.04B	$ 763.74M	420.69T
34	
OKB
OKB
OKB
$ 47.90	-1.26%	-6.37%	6.60%	-3.84%	$ 2.87B	$ 8.51M	60.00M
35	
Mantle
MNT
Mantle
$ 0.793666	-0.84%	-6.21%	7.29%	-37.22%	$ 2.67B	$ 97.17M	3.36B
36	
Cronos
CRO
Cronos
$ 0.100368	-3.32%	21.69%	38.22%	-30.53%	$ 2.67B	$ 55.79M	26.57B
37	
Internet Computer
ICP
Internet Computer
$ 5.36	0.55%	-11.29%	-16.55%	-47.12%	$ 2.58B	$ 91.65M	481.43M
38	
Ethereum Classic
ETC
Ethereum Classic
$ 16.88	1.48%	-7.76%	-11.45%	-34.54%	$ 2.55B	$ 362.66M	151.02M
39	
Aave
AAVE
Aave
$ 161.04	-1.64%	-16.07%	-14.46%	-49.09%	$ 2.43B	$ 548.53M	15.09M
40	
First Digital USD
FDUSD
First Digital USD
$ 0.998461	-0.08%	-0.02%	-0.09%	-0.09%	$ 2.10B	$ 4.98B	2.10B
41	
Official Trump
TRUMP
Official Trump
$ 10.17	0.27%	-13.44%	-22.32%		$ 2.03B	$ 506.97M	200.00M
42	
VeChain
VET
VeChain
$ 0.022789	0.08%	-13.83%	-17.57%	-48.89%	$ 1.96B	$ 86.71M	85.99B
43	
GateToken
GT
GateToken
$ 22.45	0.77%	-5.60%	9.84%	34.93%	$ 1.93B	$ 11.61M	85.83M
44	
Bittensor
TAO
Bittensor
$ 223.00	-1.38%	-17.21%	-32.51%	-50.58%	$ 1.88B	$ 184.36M	8.45M
45	
Filecoin
FIL
Filecoin
$ 2.79	1.20%	-10.99%	-12.36%	-44.87%	$ 1.79B	$ 206.16M	642.47M
46	
Celestia
TIA
Celestia
$ 3.14	-4.62%	-14.26%	-23.54%	-34.27%	$ 1.73B	$ 163.65M	551.72M
47	
Cosmos
ATOM
Cosmos
$ 4.42	2.96%	-9.82%	-1.80%	-31.50%	$ 1.73B	$ 168.97M	390.93M
48	
Kaspa
KAS
Kaspa
$ 0.06683	1.88%	-18.43%	-13.99%	-43.15%	$ 1.73B	$ 105.51M	25.82B
49	
Algorand
ALGO
Algorand
$ 0.180035	-0.49%	-11.81%	-23.94%	-48.00%	$ 1.52B	$ 192.12M	8.47B
50	
DeXe
DEXE
DeXe
$ 17.66	-0.29%	2.09%	-2.07%	18.05%	$ 1.48B	$ 15.19M	83.73M
51	
Arbitrum
ARB
Arbitrum
$ 0.33204	0.14%	-14.42%	-18.91%	-55.28%	$ 1.47B	$ 200.64M	4.42B
52	
Sonic
S
Sonic
$ 0.480346	-1.79%	-19.88%	-34.37%	-41.01%	$ 1.38B	$ 242.67M	2.88B
53	
Render Token
RENDER
Render Token
$ 3.50	-0.21%	-9.03%	-6.11%	-49.79%	$ 1.37B	$ 160.51M	392.46M
54	
KuCoin Token
KCS
KuCoin Token
$ 11.16	0.56%	-1.73%	-1.90%	3.73%	$ 1.37B	$ 626,987	122.61M
55	
Story
IP
Story
$ 5.02	-4.99%	-12.74%	-7.99%		$ 1.25B	$ 260.08M	250.00M
56	
Fasttoken
FTN
Fasttoken
$ 4.01	0.02%	-0.06%	1.16%	13.62%	$ 1.22B	$ 324,310	304.85M
57	
Optimism
OP
Optimism
$ 0.746909	-0.35%	-17.17%	-28.53%	-59.42%	$ 1.21B	$ 211.44M	1.62B
58	
Jupiter
JUP
Jupiter
$ 0.439218	-9.06%	-22.68%	-40.62%	-48.12%	$ 1.18B	$ 183.91M	2.69B
59	
Polygon Ecosystem Token
POL
Polygon Ecosystem Token
$ 0.207819	1.77%	-5.23%	-23.15%	-55.70%	$ 1.18B	$ 320.68M	5.67B
60	
Ethena
ENA
Ethena
$ 0.354895	-3.91%	-11.22%	-9.73%	-62.11%	$ 1.14B	$ 409.03M	3.22B
61	
Maker
MKR
Maker
$ 1,317.20	3.57%	3.83%	-19.19%	-13.63%	$ 1.12B	$ 133.47M	852,206
62	
Artificial Superintelligence Alliance
FET
Artificial Superintelligence Alliance
$ 0.459401	-2.92%	-16.30%	-27.49%	-64.82%	$ 1.10B	$ 153.18M	2.39B
63	
Ondo Finance
ONDO
Ondo Finance
$ 0.78901	-0.52%	-11.91%	-21.23%	-43.37%	$ 1.10B	$ 309.99M	1.39B
64	
XDC Network
XDC
XDC Network
$ 0.0688	4.03%	-7.03%	-14.48%	-6.52%	$ 1.08B	$ 36.73M	15.69B
65	
MetaGamesCoin
MGC
MetaGamesCoin
$ 0.925086	0.36%	0.85%	13.55%	84.19%	$ 1.02B	$ 840,884	1.10B
66	
Movement
MOVE
Movement
$ 0.408951	-5.65%	-5.61%	-5.42%	-52.48%	$ 981.48M	$ 164.07M	2.40B
67	
EOS
EOS
EOS
$ 0.621765	4.81%	9.02%	12.96%	-21.99%	$ 964.26M	$ 742.66M	1.55B
68	
Stacks
STX
Stacks
$ 0.617271	-0.54%	-10.03%	-22.76%	-60.81%	$ 935.67M	$ 50.86M	1.52B
69	
Bonk
BONK
Bonk
$ 0.00001129	0.25%	-20.77%	-15.29%	-64.39%	$ 877.53M	$ 90.48M	77.73T
70	
Injective
INJ
Injective
$ 8.76	-0.21%	-16.54%	-31.55%	-56.64%	$ 866.99M	$ 149.04M	98.97M
71	
Worldcoin
WLD
Worldcoin
$ 0.784959	0.62%	-15.04%	-27.48%	-63.52%	$ 852.37M	$ 259.05M	1.09B
72	
The Graph
GRT
The Graph
$ 0.088956	-0.59%	-12.81%	-23.83%	-57.05%	$ 849.40M	$ 51.91M	9.55B
73	
Flare
FLR
Flare
$ 0.014113	6.73%	-3.93%	-13.16%	-45.29%	$ 841.00M	$ 15.24M	59.59B
74	
Quant
QNT
Quant
$ 68.74	-1.26%	-12.55%	-25.71%	-36.62%	$ 829.88M	$ 27.48M	12.07M
75	
Sei
SEI
Sei
$ 0.174067	-1.91%	-14.30%	-29.34%	-57.46%	$ 810.72M	$ 135.02M	4.66B
76	
Immutable X
IMX
Immutable X
$ 0.53168	-2.71%	-14.68%	-23.87%	-61.71%	$ 788.13M	$ 73.74M	1.48B
77	
Tether Gold
XAUT
Tether Gold
$ 3,162.61	1.53%	4.41%	9.95%	20.02%	$ 779.66M	$ 28.05M	246,524
78	
Lido DAO Token
LDO
Lido DAO Token
$ 0.867801	0.66%	-19.27%	-29.32%	-53.42%	$ 774.36M	$ 121.78M	892.32M
79	
PayPal USD
PYUSD
PayPal USD
$ 0.998836	0.01%	-0.13%	0.07%	0.19%	$ 767.81M	$ 12.13M	768.71M
80	
Berachain
BERA
Berachain
$ 6.85	-6.48%	-11.72%	-16.55%		$ 736.24M	$ 306.21M	107.48M
81	
USDD
USDD
USDD
$ 1.00002	0.01%	-0.12%	-0.14%	-0.06%	$ 735.05M	$ 5.63M	735.04M
82	
Theta Token
THETA
Theta Token
$ 0.809672	-1.84%	-16.91%	-28.28%	-65.87%	$ 704.82M	$ 83.54M	870.50M
83	
Jito
JTO
Jito
$ 2.31	5.27%	2.26%	-4.01%	-31.11%	$ 697.32M	$ 96.20M	301.87M
84	
Tezos
XTZ
Tezos
$ 0.6623	1.00%	-7.20%	-11.22%	-50.46%	$ 684.36M	$ 35.04M	1.03B
85	
Ultima
ULTIMA
Ultima
$ 18,182	-4.67%	-14.72%	0.72%	171.56%	$ 680.17M	$ 15.41M	37,409
86	
The Sandbox
SAND
The Sandbox
$ 0.273848	1.33%	-8.64%	-12.42%	-51.84%	$ 674.86M	$ 67.33M	2.46B
87	
Nexo
NEXO
Nexo
$ 1.04343	-2.99%	-10.76%	-7.62%	-20.32%	$ 674.21M	$ 10.20M	646.15M
88	
PAX Gold
PAXG
PAX Gold
$ 3,151.06	0.58%	4.20%	10.13%	19.58%	$ 660.34M	$ 136.67M	209,561
89	
Frax
FRAX
Frax
$ 1.002315	0.69%	1.65%	-0.02%	3.37%	$ 650.94M	$ 752,506	649.43M
90	
BitTorrent
BTT
BitTorrent
$ 0.0₆6653	-1.54%	-5.72%	-8.42%	-38.52%	$ 644.18M	$ 21.34M	968.25T
91	
Zcash
ZEC
Zcash
$ 38.99	8.05%	20.09%	3.59%	-33.74%	$ 636.64M	$ 97.60M	16.33M
92	
Curve DAO Token
CRV
Curve DAO Token
$ 0.498653	3.94%	-0.77%	17.07%	-46.05%	$ 634.82M	$ 408.34M	1.27B
93	
Bitcoin SV
BSV
Bitcoin SV
$ 31.82	0.23%	-9.06%	-7.84%	-38.51%	$ 631.13M	$ 77.43M	19.83M
94	
IOTA
IOTA
IOTA
$ 0.171911	-0.17%	-9.99%	-13.93%	-41.01%	$ 630.86M	$ 30.18M	3.67B
95	
Kaia
KAIA
Kaia
$ 0.103497	0.24%	-6.26%	-13.47%	-49.56%	$ 617.00M	$ 13.82M	5.96B
96	
Flow
FLOW
Flow
$ 0.383572	0.38%	-10.57%	-17.92%	-46.33%	$ 601.49M	$ 39.08M	1.57B
97	
Virtual Protocol
VIRTUAL
Virtual Protocol
$ 0.587239	-4.26%	-27.32%	-44.08%	-85.33%	$ 587.24M	$ 144.28M	1,000.00M
98	
GALA
GALA
GALA
$ 0.015442	-0.24%	-15.06%	-19.38%	-56.72%	$ 584.36M	$ 192.16M	37.84B
99	
Ethereum Name Service
ENS
Ethereum Name Service
$ 15.96	0.37%	-10.16%	-24.35%	-52.86%	$ 568.15M	$ 89.42M	35.60M
100	
Floki Inu
FLOKI
Floki Inu
$ 0.00005895	2.05%	-12.24%	-25.76%	-67.45%	$ 563.52M	$ 86.42M	9.56T

"""

lines = raw_data.strip().split('\n')
result = []

for i in range(0, len(lines), 5):
    try:
        rank = int(lines[i].strip())
        name = lines[i + 1].strip()
        symbol = lines[i + 2].strip()
        raw_line = lines[i + 4].replace('\u202f', '').replace(',', '').strip()
        parts = re.split(r'\t+', raw_line)

        # Fill missing parts with "0" to avoid IndexError
        while len(parts) < 8:
            parts.append("0")

        # Clean numeric strings
        def clean_num(s):
            s = s.translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789"))
            return s.replace('$', '').replace(',', '').replace(' ', '').strip()

        def parse_abbreviated_number(s):
            s = clean_num(s)
            multiplier = 1
            if s.endswith('T'):
                multiplier = 1e12
                s = s[:-1]
            elif s.endswith('B'):
                multiplier = 1e9
                s = s[:-1]
            elif s.endswith('M'):
                multiplier = 1e6
                s = s[:-1]
            try:
                return float(s) * multiplier
            except:
                return 0.0

        try:
            price_usd = float(clean_num(parts[0]))
        except:
            price_usd = 0.0

        try:
            percent_change_1h = float(parts[1].replace('%', ''))
        except:
            percent_change_1h = 0.0

        try:
            percent_change_24h = float(parts[2].replace('%', ''))
        except:
            percent_change_24h = 0.0

        try:
            percent_change_7d = float(parts[3].replace('%', ''))
        except:
            percent_change_7d = 0.0

        market_cap_usd = parse_abbreviated_number(parts[5])
        volume_24h_usd = parse_abbreviated_number(parts[6])

        result.append({
            "name": name,
            "symbol": symbol,
            "rank": rank,
            "market_cap_usd": market_cap_usd,
            "price_usd": price_usd,
            "percent_change_1h": percent_change_1h,
            "percent_change_24h": percent_change_24h,
            "percent_change_7d": percent_change_7d,
            "volume_24h_usd": volume_24h_usd
        })

    except Exception as e:
        print(f"⚠️ Unexpected error processing entry: {lines[i:i + 5]}")
        print(f"Details: {str(e)}")

# Save to JSON
directory = r'C:/Users/khuwa/Cse_Project/coin_market_cap_top_50/March Data'
filename = 'data_3_31_2025.json'
file_path = os.path.join(directory, filename)

with open(file_path, 'w') as json_file:
    json.dump(result, json_file, indent=4)

print(f"✅ Data saved to {file_path}")