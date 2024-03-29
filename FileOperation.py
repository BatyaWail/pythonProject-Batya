import sys
from datetime import datetime
import random
from typing import List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
class FileOperation:
    #1
    def read_csv(self,file_path:str):
        return pd.read_csv(file_path)
    #2
    # def save_to_execl(self,data,file_name:str):
    #     return pd.DataFrame(data)
    def save_to_execl(self, data, file_name: str):
        # Save data to Excel file
        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False)  # Save DataFrame to Excel without index


class SalesData:
    def __init__(self,path:str):
        #self.df=FileOperation.read_csv(path)
        x=FileOperation()
        self.df=x.read_csv(path)
        self.numpy_array = self.df.values


    #4
    def eliminate_duplicates(self):
        # df=FileOperation.read_csv("YafeNof.csv")
        # csvFile.drop_duplicates(inplace=True)
        self.df.drop_duplicates(inplace=True)
     #5
    def calculate_total_sales(self):
        return self.df['Total']
    #6

    def calculate_total_sales_per_month(self):
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d.%m.%Y',errors='coerce')
        # Group by month and calculate the sum of 'Total' for each month
        monthly_sum = self.df.groupby(self.df['Date'].dt.month)['Total'].sum()
        return monthly_sum

    #7
    #def identify_best_selling_product(self):
       # maxProudact = self.df.groupby(self.df.product)["Quantity"]
       # maxProudact=max(maxProudact.sum())
       # return maxProudact
    def identify_best_selling_product(self):
        # Group by product and sum the quantities sold
        product_sales = self.df.groupby('Product')['Quantity'].sum()
        # Find the product with the maximum total quantity sold
        best_selling_product = product_sales.idxmax()
        # Return the name of the best-selling product
        return best_selling_product

   #8
    def identify_month_with_highest_sales(self):
        maxMonth= self.calculate_total_sales_per_month()
        return  max(maxMonth)

   #9
    def analys_sales_data(self):
        x=self.identify_best_selling_product()
        y=self.identify_month_with_highest_sales()
        dictionary=dict(best_selling_product= x, month_with_highest_sales= y )
        return dictionary
    #10
    def add_to_dict_minimest_seling_and_avg(self):
        product_sales = self.df.groupby('Product')['Quantity'].sum()
        # Find the product with the maximum total quantity sold
        less_selling_product = product_sales.idxmin()
        # Return the name of the best-selling product

        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d.%m.%Y',errors='coerce')
        # Group by month and calculate the sum of 'Total' for each month
        monthly_sum = self.df.groupby(self.df['Date'].dt.month)['Total'].mean()
        dictionary=self.analys_sales_data()
        dictionary['monthly_sum'] = monthly_sum
        dictionary['less_selling_product'] = less_selling_product
        return dictionary

    #task 3
    #11

    def calculate_cumulative_sales(self):
        # Convert 'Date' column to datetime type if it's not already
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d.%m.%Y')

        # Calculate the product of 'Quantity' and 'Price'
        self.df['Total_Sales'] = self.df['Quantity'] * self.df['Price']

        # Group by 'Product' and month, and calculate the cumulative sum of 'Total_Sales' for each group
        cumulative_sales = self.df.groupby(['Product', self.df['Date'].dt.month])['Total_Sales'].sum().groupby(
            level=0).cumsum()

        return cumulative_sales

    #mybe good
    # def calculate_cumulative_sales(self):
    #     # Convert 'Date' column to datetime type if it's not already
    #     self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d.%m.%Y')
    #
    #     # Calculate the product of 'Quantity' and 'Price' and store it in a new column named 'Total'
    #     self.df['Total'] = self.df['Price'] * self.df['Quantity']
    #
    #     # Group by 'Product' and 'Date', and calculate the total sales for each group
    #     monthly_sales = self.df.groupby(['Product', self.df['Date'].dt.month])['Total'].sum()#.reset_index()
    #
    #     # Calculate the cumulative sum of sales for each product across months
    #     cumulative_sales = monthly_sales.groupby('Product')['Total'].cumsum()
    #
    #     return cumulative_sales
    #12
    def calculate_90_percent_values(self):
        self.df['Discount'] = np.round((self.df['Total'] * 0.9))
        return self.df
    #13
        # sns.get_dataset_names()
    # def bar_chart_category_sum(self):
    #     # sns.get_dataset_names()
    #
    #     sns.lineplot(x='Product', y=self.df.calculate_total_sales() ,data=self.df)
    #     y=self.calculate_total_sales()
    #     sns.lineplot(x='Product', y='Total', data=self.df)
    #     plt.show()
    def bar_chart_category_sum(self):
        # Calculate the sum of quantities sold for each product
        product_sales = self.df.groupby('Product')['Quantity'].sum().reset_index()

        # Plot a line chart
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='Product', y='Quantity', data=product_sales, marker='o')
        plt.title('Sum of Quantities Sold for Each Product')
        plt.xlabel('Product')
        plt.ylabel('Sum of Quantity Sold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    def calculate_mean_quantity(self):
        try:
            sorted_indices = np.argsort(-self.numpy_array[:, 5])  # Assuming 'Total' is the 6th column (index 5)
            # Sort the numpy_array using the sorted indices
            sorted_numpy_array = self.numpy_array[sorted_indices]

            # Calculate mean
            mean = np.mean(sorted_numpy_array[:, 5])  # Assuming 'Total' is the 6th column (index 5)

            # Calculate median
            median = np.median(sorted_numpy_array[:, 5])  # Assuming 'Total' is the 6th column (index 5)

            # Calculate second maximum
            max2 = np.unique(sorted_numpy_array[:, 5])[-2]  # Second maximum

            return mean, median, max2
        except Exception as e:
            print(f"<Batya&Yeudit> ",datetime.now()," >", {str(e)},"<Batya&Yeudit>")

    def filter_by_sellings_or(self):
        # Condition 1: Number of selling more than 5 or number of selling equals 0
        condition_1 = (self.df['Quantity'] > 5) | (self.df['Quantity'] == 0)
        # Combine conditions using logical AND
        filtered_df = self.df[condition_1 ]
        return filtered_df
    def filter_by_sellings_and(self):
        # Condition 2: Price above 300 $ and sold less than 2 times
        condition_2 = (self.df['Price'] > 300) & (self.df['Quantity'] < 2)

        # Combine conditions using logical AND
        filtered_df = self.df[condition_2]

        return filtered_df
    #16
    def divide_by_2(self):
        self.df['BlackFridayPrice'] = self.df['Total'] / 2
        return self.df
        # x = FileOperation()
        # self.df = x.save_to_execl()
    #17
    # def calculate_stats(self, columns: str = None):
    #     if(columns!=None):
    #         max= self.numpy_array.max(columns)
    #         sum=self.numpy_array.sum(columns)
    #         asc=self.numpy_array.__abs__(columns)
    #     else:
    #         max= self.numpy_array.max()
    #         sum=self.numpy_array.sum()
    #         asc=self.numpy_array.__abs__()
    #     return max,sum,asc
    def calculate_stats(self, columns: str = None):
        try:
            if columns is not None:
                # Calculate stats for specific columns
                column_indices = [self.df.columns.get_loc(col) for col in columns.split(',')]
                max_vals = self.numpy_array[:, column_indices].max(axis=0)
                sums = self.numpy_array[:, column_indices].sum(axis=0)
                abs_vals = np.abs(self.numpy_array[:, column_indices])
            else:
                # Calculate stats for all columns
                max_vals = self.numpy_array.max(axis=0)
                sums = self.numpy_array.sum(axis=0)
                abs_vals = np.abs(self.numpy_array)

            return max_vals, sums, abs_vals
        except Exception as e:
            print(f"<Batya&Yeudit> ",datetime.now()," >", {str(e)},"<Batya&Yeudit>")
    #18
    #def convert_date_format(self, date_columns:List=None):
        #self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d.%m.%Y %H:%M:%S')
        #return self.df
    def convert_date_format(self, date_columns: List = None):
        if date_columns is None:
            date_columns = ['Date']  # Assuming 'Date' is the name of the column containing dates

        for column in date_columns:
            #self.df[column] = pd.to_datetime(self.df[column], format='%d.%m.%Y %H:%M:%S')
            self.df[column] = pd.to_datetime(self.df[column], format='%d.%m.%Y %H:%M:%S', errors='coerce')

            print(self.df[column])
        return self.df
    #task 6
    def draw_calculate_total_sales(self):
        total_sales = self.df['Total']
        plt.bar(range(len(total_sales)), total_sales)
        plt.xlabel('Index')
        plt.ylabel('Total Sales')
        plt.title('Total Sales Data')
        plt.show()
    #not good
    def draw_calculate_total_sales_per_month(self):
        monthly_sum = self.calculate_total_sales_per_month()

        # Plotting
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        print(len(months))
        print(len(monthly_sum))
        plt.bar(months, monthly_sum)
        plt.xlabel('Month')
        plt.ylabel('Total Sales')
        plt.title('Total Sales Per Month')

        plt.show()
    def draw_identify_best_selling_product(self):
        best_selling_product = self.identify_best_selling_product()

        # Group by product and sum the quantities sold
        product_sales = self.df.groupby('Product')['Quantity'].sum()

        # Plotting
        product_sales.plot(kind='bar')
        plt.xlabel('Product')
        plt.ylabel('Quantity Sold')
        plt.title('Quantity Sold for Each Product')
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.axhline(product_sales[best_selling_product], color='r', linestyle='--',
                    label='Best Selling Product')  # Highlight best-selling product
        plt.legend()
        plt.tight_layout()  # Adjust layout to prevent clipping of labels
        plt.show()
    #not good
    def draw_identify_month_with_highest_sales(self):
        max_month = self.identify_month_with_highest_sales()
        monthly_sum = self.calculate_total_sales_per_month()

        # Plotting
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        plt.bar(months, monthly_sum)
        plt.xlabel('Month')
        plt.ylabel('Total Sales')
        plt.title('Total Sales Per Month')
        plt.axvline(x=max_month - 1, color='r', linestyle='--',
                    label='Month with Highest Sales')  # Highlight month with highest sales
        plt.legend()
        plt.show()
    def draw_analys_sales_data(self):
        data = self.analys_sales_data()

        # Drawing the best selling product as a line plot
        best_selling_product = data['best_selling_product']
        product_sales = self.df.groupby('Product')['Quantity'].sum()
        product_sales.plot(kind='line', marker='o')  # Use line plot with markers
        plt.xlabel('Product')
        plt.ylabel('Quantity Sold')
        plt.title('Quantity Sold for Each Product')
        plt.xticks(rotation=45)
        plt.axhline(product_sales[best_selling_product], color='r', linestyle='--', label='Best Selling Product')
        plt.legend()
        plt.tight_layout()
        plt.show()

    def draw_add_to_dict_minimest_seling_and_avg(self):
        data = self.add_to_dict_minimest_seling_and_avg()
        product_sales = self.df.groupby('Product')['Quantity'].sum()
        less_selling_product = data['less_selling_product']
        plt.scatter(product_sales.index, product_sales.values, label='Product Sales')
        plt.scatter(less_selling_product, product_sales[less_selling_product], color='r',
                    label='Least Selling Product')  # Highlight the least selling product
        plt.xlabel('Product')
        plt.ylabel('Quantity Sold')
        plt.title('Distribution of Sales Among Products')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()
    def draw_calculate_cumulative_sales(self):
        cumulative_sales = self.calculate_cumulative_sales()

        # Reset index to access 'Product' and 'Date' columns separately
        cumulative_sales = cumulative_sales.reset_index()

        # Create a separate plot for each product
        for product, data in cumulative_sales.groupby('Product'):
            plt.plot(data['Date'], data['Total_Sales'], label=product)

        plt.xlabel('Date')
        plt.ylabel('Cumulative Sales')
        plt.title('Cumulative Sales Over Time')
        plt.legend()
        plt.tight_layout()
        plt.show()

    def draw_calculate_mean_quantity(self):
        mean, median, max2 = self.calculate_mean_quantity()
        quantities = [mean, median, max2]

        plt.boxplot(quantities, vert=False)
        plt.yticks([1, 2, 3], ['Mean', 'Median', 'Second Max'])
        plt.xlabel('Quantity')
        plt.title('Statistical Summary of Quantity')
        plt.tight_layout()
        plt.show()

    def draw_calculate_mean_quantity(self):

        mean, median, max2 = self.calculate_mean_quantity()

        # Create a list containing the three values
        quantities = [mean, median, max2]
        labels = ['Mean', 'Median', 'Second Max']

        # Create a heatmap plot
        plt.imshow([quantities], cmap='viridis', aspect='auto')

        # Add labels and title
        plt.xlabel('Statistical Measure')
        plt.ylabel('Values')
        plt.title('Statistical Summary of Quantity')

        # Customize the x-axis tick labels
        plt.xticks(np.arange(len(labels)), labels)

        # Add color bar
        plt.colorbar(label='Quantity')

        # Add numerical values to the heatmap plot
        for i in range(len(quantities)):
            plt.text(i, 0, f'{quantities[i]:.2f}', color='black', ha='center', va='center')

        # Show plot
        plt.show()

    def draw_filter_by_sellings_or(self):
        filtered_df = self.filter_by_sellings_or()

        # Count the occurrences of each condition
        count_more_than_5 = filtered_df[filtered_df['Quantity'] > 5].shape[0]
        count_equals_0 = filtered_df[filtered_df['Quantity'] == 0].shape[0]

        # Create labels for the pie chart
        labels = ['More than 5', 'Equals 0']
        sizes = [count_more_than_5, count_equals_0]

        # Plot the pie chart
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)

        # Equal aspect ratio ensures that pie is drawn as a circle
        plt.axis('equal')

        # Add a title
        plt.title('Distribution of Filtered Data')

        # Show plot
        plt.show()
    def draw_filter_by_sellings_and(self):
        filtered_df = self.filter_by_sellings_and()

        # Assuming there's a suitable categorical variable in the dataframe
        categorical_variable = filtered_df['Some_Column']  # Replace 'Some_Column' with the actual column name

        # Count the occurrences of each category
        category_counts = categorical_variable.value_counts()

        # Create a sorted list of unique categories
        categories = sorted(category_counts.index)

        # Calculate the cumulative sum of category counts
        cumulative_counts = category_counts[categories].cumsum()

        # Plot the area plot
        plt.fill_between(categories, cumulative_counts, color='skyblue', alpha=0.4)

        # Add labels and title
        plt.xlabel('Category')
        plt.ylabel('Cumulative Count')
        plt.title('Cumulative Distribution of Filtered Data')

        # Show plot
        plt.show()

    def draw_divide_by_2(self):

        original_total = self.df['Total']
        black_friday_price = self.divide_by_2()[
            'BlackFridayPrice']  # Assuming 'BlackFridayPrice' is created by divide_by_2 function

        # Plot the scatter plot
        plt.scatter(range(len(original_total)), original_total, label='Original Total')
        plt.scatter(range(len(black_friday_price)), black_friday_price, label='Black Friday Price')

        # Draw lines connecting points for the same product
        for index, row in self.df.iterrows():
            product = row['Product']
            original_point = original_total[index]
            black_friday_point = black_friday_price[index]
            plt.plot([index, index], [original_point, black_friday_point], color='gray', linestyle='--', linewidth=0.5)

        # Set x-axis labels as product names
        plt.xticks(range(len(self.df)), self.df['Product'], rotation=90)

        # Add labels and title
        plt.xlabel('Product')
        plt.ylabel('Total')
        plt.title('Comparison of Original Total and Black Friday Price')

        # Add legend
        plt.legend()

        # Show plot
        plt.show()
    # seabron
    # def draw_calculate_stats(self, columns: str = None):
    #     max_vals, sums, abs_vals = self.calculate_stats(columns)
    #
    #     # Create a DataFrame from the statistics
    #     stats_df = pd.DataFrame({'Max': max_vals, 'Sum': sums, 'Abs': abs_vals})
    #
    #     # Plot the statistics using Seaborn
    #     sns.set(style="whitegrid")
    #     ax = sns.barplot(data=stats_df, orient='h')
    #
    #     # Add labels and title
    #     ax.set_xlabel('Value')
    #     ax.set_ylabel('Statistics')
    #     ax.set_title('Statistics Summary')
    #
    #     # Show plot
    #     plt.show()
    def draw_calculate_stats(self, columns: str = None):
        max_vals, sums, abs_vals = self.calculate_stats(columns)

        # Create a DataFrame from the statistics
        stats_df = pd.DataFrame({'Max': max_vals, 'Sum': sums, 'Abs': abs_vals})

        # Plot the statistics using Seaborn
        sns.set(style="whitegrid")
        ax = sns.barplot(data=stats_df, orient='h')

        # Add labels and title
        ax.set_xlabel('Value')
        ax.set_ylabel('Statistics')
        ax.set_title('Statistics Summary')

        # Show plot
        plt.show()

    # def draw2_identify_best_selling_product(self):
    #     best_selling_product = self.identify_best_selling_product()
    #
    #     # Get the quantity sold for the best-selling product
    #     quantity_sold = self.df.groupby('Product')['Quantity'].sum()[best_selling_product]
    #
    #     # Create a pie chart
    #     plt.figure(figsize=(8, 8))
    #     plt.pie([quantity_sold, sum(self.df['Quantity']) - quantity_sold],
    #             labels=[best_selling_product, 'Other Products'],
    #             autopct='%1.1f%%', startangle=140)
    #     plt.title('Best-Selling Product')
    #
    #     # Show plot
    #     plt.show()
    def draw2_identify_best_selling_product(self):
        # Count the occurrences of each product
        product_counts = self.df['Product'].value_counts()

        # Create a DataFrame from the product counts
        product_counts_df = pd.DataFrame({'Product': product_counts.index, 'Frequency': product_counts.values})

        # Set the style
        sns.set(style="whitegrid")

        # Plot the line plot for all products using Seaborn
        plt.figure(figsize=(10, 6))
        ax = sns.lineplot(x='Product', y='Frequency', data=product_counts_df)

        # Rotate the x-axis labels for better readability
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

        # Add labels and title
        ax.set_xlabel('Product')
        ax.set_ylabel('Frequency')
        ax.set_title('Product Sales Distribution')

        # Show plot
        plt.show()

    def draw2_analys_sales_data(self):
        # Perform analysis
        analysis_dict = self.analys_sales_data()

        # Convert dictionary to DataFrame for plotting
        df_analysis = pd.DataFrame(analysis_dict.items(), columns=['Metric', 'Value'])

        # Set the style
        sns.set(style="whitegrid")

        # Plot the strip plot
        plt.figure(figsize=(8, 6))
        ax = sns.stripplot(x='Value', y='Metric', data=df_analysis, jitter=True)

        # Add labels and title
        ax.set_xlabel('Value')
        ax.set_ylabel('Metric')
        ax.set_title('Analysis of Sales Data')

        # Show plot
        plt.show()

    def draw2_cumulative_sales(self):
        # Perform calculations
        cumulative_sales = self.calculate_cumulative_sales()

        # Convert Series to DataFrame
        df_cumulative_sales = cumulative_sales.reset_index()

        # Rename columns for better readability
        df_cumulative_sales.columns = ['Product', 'Month', 'Cumulative Sales']

        # Create a line plot with Seaborn
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df_cumulative_sales, x='Month', y='Cumulative Sales', hue='Product', marker='o')

        # Set labels and title
        plt.xlabel('Month')
        plt.ylabel('Cumulative Sales')
        plt.title('Cumulative Sales Over Time')

        # Show plot
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    def draw2_90_percent_values(self):

        discount_values = self.calculate_90_percent_values()

        # Create a violin plot to visualize the distribution of 90% discount values
        sns.violinplot(discount_values, inner="point")
        plt.title('Violin Plot of 90% Discount Values')
        plt.xlabel('Discount')
        plt.show()

    def visualize_mean_quantity(self, mean, median, max2):
        # Create a bar plot to visualize the calculated values
        sns.barplot(x=['Mean', 'Median', 'Second Max'], y=[mean, median, max2])
        plt.title('Mean, Median, and Second Maximum Quantity')
        plt.ylabel('Quantity')
        plt.show()

    def draw2_mean_quantity(self):
        mean, median, max2 = self.calculate_mean_quantity()
        self.visualize_mean_quantity(mean, median, max2)

    # def draw2_filter_by_sellings_and(self):
    #     filtered_df = self.filter_by_sellings_and()
    #
    #     # Create a countplot to visualize the filtered DataFrame
    #     plt.figure(figsize=(10, 6))
    #     sns.countplot(data=filtered_df, x='Column_Name_To_Visualize')
    #     plt.title('Filtered Data by Sellings and Price')
    #     plt.xlabel('X-axis label')
    #     plt.ylabel('Y-axis label')
    #     plt.show()
    def seaborn2(self):
        try:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=self.df, x='Price', y='Quantity')
            plt.title('Scatter Plot of Price vs. Quantity (Seaborn)')
            plt.xlabel('Price')
            plt.ylabel('Quantity')
            plt.show()
        except Exception as e:
            print(f"<Batya&Yeudit> ",datetime.now()," >", {str(e)},"<Batya&Yeudit>")


# 3. Seaborn Bar Plot
    def Seaborn_Bar_Plot(self):
        try:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=self.df, x='Product', y='Quantity')
            plt.title('Total Sales per Product (Seaborn)')
            plt.xlabel('Product')
            plt.ylabel('Total Sales Quantity')
            plt.xticks(rotation=45)
            plt.show()
        except Exception as e:
            print(f"<Batya&Yeudit> ",datetime.now()," >", {str(e)},"<Batya&Yeudit>")

    def Seaborn_Box_Plot(self):
        try:
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=self.df, x='Product', y='Total')
            plt.title('Box Plot of Total Sales per Product (Seaborn)')
            plt.xlabel('Product')
            plt.ylabel('Total Sales')
            plt.xticks(rotation=45)
            plt.show()
        except Exception as e:
            print(f"<Batya&Yeudit> "+datetime.datetime()+" >"+ {str(e)}+"<Batya&Yeudit>")

    def draw_sales_and_highest_amount(product_name, sales_data):
        product_sales = sales_data[sales_data['Product'] == product_name]['Quantity']
        highest_amount = sales_data[sales_data['Product'] == product_name]['Total'].max()
        drawn_number = np.random.choice(product_sales)
        return drawn_number, highest_amount

