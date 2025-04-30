# Daily Crypto Prediction

This project fetches daily cryptocurrency data and uses AI to predict the following day's Bitcoin price, market sentiment, and portfolio recommendations. It is intended for research and evaluation of AI-based forecasting techniques in financial markets.

## Table of Contents
- [Overview](#overview)  
- [Project Structure](#project-structure)  
- [How to Run](#how-to-run)  
- [Results](#results)  
- [Handling Missed Data](#handling-missed-data)  

## Overview

This repository automates:
- Fetching raw crypto market data using the CoinMarketCap API
- Generating next-day predictions using the Perplexity API
- Saving and organizing results for analysis in JSON and Excel formats

It supports daily use, but also includes tools for fetching historical data if a day was missed.

## Project Structure

```
├── getDailyPredictions.py         # Main script to fetch data and generate predictions
├── March_Data/                    # Raw market data (daily JSON files)
├── Predicted_Price/               # AI-generated Bitcoin price predictions (T+1)
├── Market_Sentiment/             # AI-generated sentiment: Bullish, Neutral, Bearish (T+1)
├── Portfolio/                     # AI-generated portfolio suggestions (T+1)
├── Results/                       # Evaluation and visualization outputs
│   ├── Actual_vs_Predicted_Bitcoin.py
│   ├── Analysis.py
│   ├── Bargraph.py
│   ├── Heapmap.py
│   └── transfer_to_excel.py
├── Excel_for_March_2025.xlsx     # Final consolidated Excel output
├── To_run_past_data/             # Tools to fetch data for missed days
```

## How to Run

1. Clone the repository
2. **Run the daily prediction script**
   ```
   python getDailyPredictions.py
   ```
   This script will:
   - Fetch real-time market data from CoinMarketCap
   - Generate predictions for the *next day* using AI prompts
   - Save the results in the corresponding folders as JSON files

3. **Understand the output**
   - If run on `January 5`, predictions will be for `January 6`
   - Three folders are populated:
     - `Predicted_Price`: Price prediction (T+1)
     - `Market_Sentiment`: Market trend classification (T+1)
     - `Portfolio`: Buy/Sell/Hold recommendations (T+1)

4. **Raw data**
   - Stored in `March_Data` as daily JSON files

## Results

To evaluate and visualize model performance:

- `Results/Actual_vs_Predicted_Bitcoin.png`: Line graph comparing real vs. predicted price  
- `Results/Analysis.txt`: Accuracy metrics like precision and recall  
- `Results/Bargraph.png`: Visual summary of model performance  
- `Results/Heapmap.png`: Correlation matrix of features  
- `transfer_to_excel.py`: Converts all raw and predicted data to an Excel sheet

Final results can be viewed in `Excel_for_March_2025.xlsx`.

## Handling Missed Data

If you forget to run predictions on certain days, use the tools in `To_run_past_data/`. These scripts fetch historical data from:
```
https://coincodex.com/historical-data/crypto/
```

