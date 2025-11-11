# Reads uploaded files

import pandas as pd
import io

def load_demo_dataset(industry):
    if industry == "Retail Sales":
        return pd.read_csv("data/retail_demo.csv")
    elif industry == "Finance/Loan Analytics":
        return pd.read_csv("data/finance_demo.csv")
    elif industry == "Healthcare Service Performance":
        return pd.read_csv("data/healthcare_demo.csv")
    else:
        return pd.DataFrame()

async def load_user_data(uploaded_file):
    # await reading bytes
    file_bytes = await uploaded_file.read()
    file_name = uploaded_file.filename  # FIX: use .filename, not .name

    # decode bytes safely
    try:
        s = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        s = file_bytes.decode("latin1")

    # load into dataframe
    df = pd.read_csv(io.StringIO(s), header=0)

    # clean column names
    df.columns = df.columns.str.replace(u"\xa0", u" ", regex=True).str.strip()

    # drop completely empty rows
    df.dropna(how="all", inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df, file_name

# Row ID	Order ID	Order Date	Ship Date	Ship Mode	Customer ID	Customer Name	Segment	Country	City	State	Postal Code	Region	Product ID	Category	Sub-Category	Product Name	Sales	Quantity	Discount	Profit
# 1	CA-2016-152156	11/08/2016	11/11/2016	Second Class	CG-12520	Claire Gute	Consumer	United States	Henderson	Kentucky	42420	South	FUR-BO-10001798	Furniture	Bookcases	Bush Somerset Collection Bookcase	261.96	2	0	41.9136
# 2	CA-2016-152156	11/08/2016	11/11/2016	Second Class	CG-12520	Claire Gute	Consumer	United States	Henderson	Kentucky	42420	South	FUR-CH-10000454	Furniture	Chairs	Hon Deluxe Fabric Upholstered Stacking Chairs, Rounded Back	731.94	3	0	219.582
# 3	CA-2016-138688	06/12/2016	6/16/2016	Second Class	DV-13045	Darrin Van Huff	Corporate	United States	Los Angeles	California	90036	West	OFF-LA-10000240	Office Supplies	Labels	Self-Adhesive Address Labels for Typewriters by Universal	14.62	2	0	6.8714
# 4	US-2015-108966	10/11/2015	10/18/2015	Standard Class	SO-20335	Sean O'Donnell	Consumer	United States	Fort Lauderdale	Florida	33311	South	FUR-TA-10000577	Furniture	Tables	Bretford CR4500 Series Slim Rectangular Table	957.5775	5	0.45	-383.031
# 5	US-2015-108966	10/11/2015	10/18/2015	Standard Class	SO-20335	Sean O'Donnell	Consumer	United States	Fort Lauderdale	Florida	33311	South	OFF-ST-10000760	Office Supplies	Storage	Eldon Fold 'N Roll Cart System	22.368	2	0.2	2.5164
# 6	CA-2014-115812	06/09/2014	6/14/2014	Standard Class	BH-11710	Brosina Hoffman	Consumer	United States	Los Angeles	California	90032	West	FUR-FU-10001487	Furniture	Furnishings	Eldon Expressions Wood and Plastic Desk Accessories, Cherry Wood	48.86	7	0	14.1694
# 7	CA-2014-115812	06/09/2014	6/14/2014	Standard Class	BH-11710	Brosina Hoffman	Consumer	United States	Los Angeles	California	90032	West	OFF-AR-10002833	Office Supplies	Art	Newell 322	7.28	4	0	1.9656
# 8	CA-2014-115812	06/09/2014	6/14/2014	Standard Class	BH-11710	Brosina Hoffman	Consumer	United States	Los Angeles	California	90032	West	TEC-PH-10002275	Technology	Phones	Mitel 5320 IP Phone VoIP phone	907.152	6	0.2	90.7152
# 9	CA-2014-115812	06/09/2014	6/14/2014	Standard Class	BH-11710	Brosina Hoffman	Consumer	United States	Los Angeles	California	90032	West	OFF-BI-10003910	Office Supplies	Binders	DXL Angle-View Binders with Locking Rings by Samsill	18.504	3	0.2	5.7825
# 10	CA-2014-115812	06/09/2014	6/14/2014	Standard Class	BH-11710	Brosina Hoffman	Consumer	United States	Los Angeles	California	90032	West	OFF-AP-10002892	Office Supplies	Appliances	Belkin F5C206VTEL 6 Outlet Surge	114.9	5	0	34.47
