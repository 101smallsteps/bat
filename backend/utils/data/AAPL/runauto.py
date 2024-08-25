import subprocess
import os 
import datetime
from dotenv import load_dotenv


symbols=['AAPL']

done=[]

quarterly_in_action=[
                        {
                            'quarter':'Q_3',
                            'date':'2023-09-30',
                        }
                    ]
quarterly_in_action_1=[
                        {
                            'quarter':'Q_3',
                            'date':'2023-09-30',
                        },
                        {
                            'quarter':'Q_4',
                            'date':'2023-12-31',
                        },
                        {
                            'quarter':'Q_1',
                            'date':'2024-03-31',
                        },
                        {
                            'quarter':'Q_2',
                            'date':'2024-06-30',
                        },                        
                    ]

load_dotenv('/home/aarth/bat/backend/utils/.env')
for sym in symbols:
    for qtr in quarterly_in_action:
        yr=1111
        try:
            date_obj = datetime.datetime.strptime(qtr['date'], "%Y-%m-%d")
            yr = date_obj.year
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")
            yr = 2222
        print(qtr)
        #register finance data for the quarter
        cmd_0=f"cd /home/aarth/bat/backend/utils;python3 update_db.py -r -dt Q -ds CREATE -sym {sym} -df {qtr['quarter']} -dy {yr} ;"
        print(f'executing {cmd_0}')
        os.system(cmd_0)
        #download data
        cmd_1=f"python3 ../../yfin.py  -sym {sym} -d {qtr['date']}"
        print(f'executing {cmd_1}') 
        os.system(cmd_1)
        #process downloaded balancesheet data csv 
        cmd_2=f"python3 ../../processCSV.py quarterly_balance_{sym}_{qtr['date']}.csv ./processed/quarterly_balance_{sym}_{qtr['date']}.csv"
        print(f'executing {cmd_2}') 
        os.system(cmd_2)
        #process downloaded cashflow  data csv
        cmd_3=f"python3 ../../processCSV.py quarterly_cash_{sym}_{qtr['date']}.csv ./processed/quarterly_cash_{sym}_{qtr['date']}.csv"
        print(f'executing {cmd_3}')
        os.system(cmd_3)
        #process downloaded incomestmt data csv
        cmd_4=f"python3 ../../processCSV.py quarterly_incomestmt_{sym}_{qtr['date']}.csv ./processed/quarterly_incomestmt_{sym}_{qtr['date']}.csv"
        print(f'executing {cmd_4}')
        os.system(cmd_4)
        #update DB
        cmd_5_1=f"cd /home/aarth/bat/backend/utils;python3 update_db.py -s IncomeStatement  -dt Q -ds CREATE -sym {sym} -df {qtr['quarter']} -dy {yr} -ip ./data/{sym}/processed/quarterly_incomestmt_{sym}_{qtr['date']}.csv;"
        print(f'executing {cmd_5_1}')
        os.system(cmd_5_1)
        cmd_5_2=f"cd /home/aarth/bat/backend/utils;python3 update_db.py -s BalanceSheet  -dt Q -ds CREATE -sym {sym} -df {qtr['quarter']} -dy {yr} -ip ./data/{sym}/processed/quarterly_balance_{sym}_{qtr['date']}.csv;"
        print(f'executing {cmd_5_2}')
        os.system(cmd_5_2)
        cmd_5_3=f"cd /home/aarth/bat/backend/utils;python3 update_db.py -s CashFlow  -dt Q -ds CREATE -sym {sym} -df {qtr['quarter']} -dy {yr} -ip ./data/{sym}/processed/quarterly_cash_{sym}_{qtr['date']}.csv;"
        print(f'executing {cmd_5_3}')
        os.system(cmd_5_3)
        #perform analysis 
        cmd_6=f"cd /home/aarth/bat/backend/utils;python3 perform_analysis.py;"
        print(f'executing {cmd_6}')
        os.system(cmd_6)
        #perform calculations
        cmd_7_1=f"cd /home/aarth/bat/backend/utils;python3 calculate_metrics.py -s IncomeStatement  -dt Q -ds CREATE -sym {sym} -df {qtr['quarter']} -dy {yr} -ip ./data/{sym}/processed/quarterly_incomestmt_{sym}_{qtr['date']}.csv;"
        print(f'executing {cmd_7_1}')
        os.system(cmd_7_1)
        cmd_7_2=f"cd /home/aarth/bat/backend/utils;python3 calculate_metrics.py -s BalanceSheet  -dt Q -ds CREATE -sym {sym} -df {qtr['quarter']} -dy {yr} -ip ./data/{sym}/processed/quarterly_balance_{sym}_{qtr['date']}.csv;"
        print(f'executing {cmd_7_2}')
        os.system(cmd_7_2)
        cmd_7_3=f"cd /home/aarth/bat/backend/utils;python3 calculate_metrics.py -s CashFlow  -dt Q -ds CREATE -sym {sym} -df {qtr['quarter']} -dy {yr} -ip ./data/{sym}/processed/quarterly_cash_{sym}_{qtr['date']}.csv;"
        print(f'executing {cmd_7_3}')
        os.system(cmd_7_3)


