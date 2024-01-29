#  STOCK SALES AND ANALYSIS

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.colors as pc

# Set the default plotly template to "plotly_white"
pio.templates.default = "plotly_white"

# Reading the csv file
df = pd.read_csv('Sample - Superstore.csv',encoding='ANSI')
print('\nORIGINAL CSV DATA\n\n',df)
print(df.describe())

# Drop unwanted columns from the given data
df.drop(['Order ID','Customer ID','Customer Name',
         'Ship Date','Ship Mode','Country','State','Postal Code',
         'Product Name','City','Product ID','Quantity','Region','Discount'],inplace=True,axis=1)
df.set_index('Row ID',inplace=True)
print('\nCLEANED DATA WITH REQUIRED COLUMNS\n\n',df)

# Convert the "Order Date" column to pandas datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Create new columns for Order Month, Order Year, Order DayOfWeek

df['Order Month'] = df['Order Date'].dt.month
df['Order Year'] = df['Order Date'].dt.year
df['Order Day of week'] = df['Order Date'].dt.dayofweek
print('\nDATA WITH NEWLY ADDED MONTH, YEAR AND DAY COLUMNS\n\n',df)

# MONTHLY DATA ANALYSIS
# Group the data by year and month and calculate the total sales and profit for each month
monthly_data_analysis = df.groupby(["Order Year", "Order Month"]).agg({"Sales": "sum", "Profit": "sum"}).reset_index()

# Rename the month numbers to month names
month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
               7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

monthly_data_analysis["Order Month"] = monthly_data_analysis["Order Month"].map(month_names)
print('\nMONTHLY DATA ANALYSIS\n\n',monthly_data_analysis)


# Creating a line chart for Monthly Sales Analysis using plotly.express
fig1 = px.line(monthly_data_analysis,
               x="Order Month",
               y="Sales",
               color="Order Year",
               title="Monthly Sales Analysis",
               labels={"Sales": "Sales Amount ($)"},
               template="plotly_white")
# Show the plot
fig1.show()


# Creating a line chart for Monthly Profit Analysis using plotly.express
fig2 = px.line(monthly_data_analysis,
               x="Order Month",
               y="Profit",
               color="Order Year",
               title="Monthly Profit Analysis",
               labels={"Profit": "Profit Amount ($)"},
               template="plotly_white")
# Show the plot
fig2.show()


# CATEGORY DATA ANALYSIS
# Group the data by category and calculate its total sales and profit
category_data_analysis = df.groupby('Category').agg({"Sales": "sum", "Profit": "sum"}).reset_index()
print('\nCATEGORY DATA ANALYSIS\n\n',category_data_analysis)

# Creating a pie chart for sales by category analysis using plotly.express
fig3 = px.pie(category_data_analysis,
              names='Category' ,
              values ='Sales',
              title = 'Category Sales Analysis' ,
              hole=0.5,
              color_discrete_sequence=px.colors.qualitative.Antique)

fig3.update_traces(textposition='inside', textinfo='percent+label')
fig3.update_layout(title_text='Sales Analysis by Category', title_font=dict(size=24))
fig3.show()

# Creating a pie chart for profit by category analysis using plotly.express
fig4 = px.pie(category_data_analysis,
              names='Category' ,
              values ='Profit',
              title = 'Category profit analysis' ,
              hole=0.5,
              color_discrete_sequence=px.colors.qualitative.Vivid)

fig4.update_traces(textposition='inside', textinfo='percent+label')
fig4.update_layout(title_text='Profit Analysis by Category', title_font=dict(size=24))
fig4.show()

# SUB-CATEGORY DATA ANALYSIS
# Group the data by sub-category and calculate its total sales and profit
subcategory_data_analysis = df.groupby("Sub-Category").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
print('\nSUB_CATEGORY DATA ANALYSIS\n\n',subcategory_data_analysis)

# Creating a bar chart for sales by sub-category analysis using plotly.express
fig5 = px.bar(subcategory_data_analysis,
              x="Sub-Category",
              y="Sales",
              title='Sub Category Sales Analysis',
              labels={'Sub-Category' : 'Products'})
fig5.show()

# Creating a bar chart for profit by sub-category analysis using plotly.express
fig6 = px.bar(subcategory_data_analysis,
              x="Sub-Category",
              y='Profit',
              title='Sub Category Profit Analysis',
              labels={'Sub-Category' : 'Products'})
fig6.show()

# CUSTOMER SEGMENT DATA ANALYSIS
# Group the data by segment and calculate its total sales and profit
segment_data_analysis = df.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
# Creating a column dedicated for sales to profit ratio
segment_data_analysis['Sales_to_Profit_Ratio'] = segment_data_analysis['Sales'] / segment_data_analysis['Profit']
print('\nCUSTOMER SEGMENT DATA ANALYSIS\n\n',segment_data_analysis)

# Create a bar chart for sales and profit by customer segment analysis
fig7 = go.Figure()
color_palette = px.colors.qualitative.Pastel
# Plot the Sales bar
fig7.add_trace(go.Bar(
    x=segment_data_analysis['Segment'],
    y=segment_data_analysis['Sales'],
    name='Sales',
    marker_color=color_palette[2]  # Customize the color of the Sales bar
))

# Plot the Profit bar next to the Sales bar
fig7.add_trace(go.Bar(
    x=segment_data_analysis['Segment'],
    y=segment_data_analysis['Profit'],
    name='Profit',
    marker_color=color_palette[9]  # Customize the color of the Profit bar
))

# Update the layout of the chart
fig7.update_layout(
    title='Segment Sales and Profit Analysis',
    xaxis_title='Customer Segments',
    yaxis_title='Capital',
    barmode='group',  # To have bars adjacent to each other
    showlegend=True,  # Show a legend with bar names
)
fig7.show()