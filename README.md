# Market-Price-Prediction-Using-Unbiased-Learning-for-Censored-Data-in-Real-Time-Bidding
MSc Project

To run the code for this project, make sure you have Python 2.7 installed. The required dependencies are Numpy, SciPy, Matplotlib and Sklearn.

There are four folders in Code folder– 'pre-processing', 'statistics', 'winning-pro- estimation' and 'market-price-prediction'. Before running the code, follow steps in make-ipinyou-data (https://github.com/wnzhang/make-ipinyou-data) to convert original iPinYou data into feature vectors, and keep 'make-ipinyou-data' folder in the same root with Code.

1. run 'simulated_data.py' in 'pre-processing' first to simulating data for each campaign with new bidding strategy. Then run 'combine_all.py' to get data for all campaigns. After that, run 'get_bo_file.py' to get a file with winning indicators (1 for win, 0 for lose) for each bid price in train set, and 'split_test_data.py' to split test set into winning and losing subset.

2. run win 'lose_ratio.py' and 'visualization.py' in 'statistics' folder to get data statistics and the visualization of the market price distribution.

3. run 'biased.py' and 'kaplan_meier.py' in 'winning-pro-estimation' for winning probabilities with UOMP and KMMP setting respectively. Then run get 'trian_wyzx_bid.py' to load true winning probability for each instance in train set, and run 'test_full_win_prob.py' get winning probabilities for FULL and TRUTH setting. Finally, run 'plot.py' to plot line graphs of winning probabilities for each campaign.

4. run 'lin_ll_bias.py' and 'lin_ll_unbias.py' in 'market-price-prediction' for routine (BIAS and FULL) and unbiased (UOMP and KMMP) training algorithm. Training log and weights of prediction model are written in files for tuning hyper- parameters. do 'prediction.py' is for predicting market price, and 'rmse_eval.py' and 'plot_rmse.py' are for evaluation with RMSE and bar chart respectively.
