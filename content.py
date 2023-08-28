"""
Telco Customer Churn Prediction: Content for Pages
"""

# Authors: Tolgahan Cepel <tolgahan.cepel@gmail.com>
# License: MIT

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

import os
import sys
import copy

from src.graphs import dist_tenure, dist_monthlycharges, dist_totalcharges

#-------------------------------------------------------------------------------
# DATA ANALYSIS
#-------------------------------------------------------------------------------

# Tenure Distribution

card_tensure = dbc.Card(
    dbc.CardBody(
        dcc.Graph(figure = dist_tenure(), config = {"displayModeBar": False}, style = {"height": "42vh"})
    ),
    style = {"background-color": "#16103a"}
)

# Monthly Charges Distribution

card_monthlycharges = dbc.Card(
    dbc.CardBody(
        dcc.Graph(figure = dist_monthlycharges(), config = {"displayModeBar": False}, style = {"height": "42vh"})          
    ),
    style = {"background-color": "#16103a"}
)

# Total Charges Distribution

card_totalcharges = dbc.Card(
    dbc.CardBody(
        dcc.Graph(figure = dist_totalcharges(), config = {"displayModeBar": False}, style = {"height": "42vh"})
    ),
    style = {"background-color": "#16103a"}
)

# Categorical Bar Chart

card_categorical = dbc.Card(
    dbc.CardBody(
        dbc.Spinner(
            size="md",
            color="light",
            children=[
                dcc.Graph(id="categorical_bar_graph", config = {"displayModeBar": False}, style = {"height": "48vh"})
            ]
        ),
        style = {"height": "52vh"}
    ),
    style = {"background-color": "#16103a"}
)

# Donut Chart

card_donut = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Spinner(size="md",color="light",
                    children=[
                        dcc.Graph(id="categorical_pie_graph", config = {"displayModeBar": False}, style = {"height": "48vh"})
                    ]
                ),
                
            ], style = {"height": "52vh"}
        ),
    ],
    style = {"background-color": "#16103a"}
)

# TABS

tab_graphs = [

    # Categorical Fetaures Visualization
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [

                            dbc.Col([
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupAddon("Categorical Feature", addon_type="prepend"),
                                        dbc.Select(
                                            options=[
                                                {"label": "Gender", "value": "gender"},
                                                {"label": "Partner", "value": "Partner"},
                                                {"label": "Dependents", "value": "Dependents"},
                                                {"label": "Phone Service", "value": "PhoneService"},
                                                {"label": "Multiple Lines", "value": "MultipleLines"},
                                                {"label": "Internet Service", "value": "InternetService"},
                                                {"label": "Online Security", "value": "OnlineSecurity"},
                                                {"label": "Online Backup", "value": "OnlineBackup"},
                                                {"label": "Device Protection", "value": "DeviceProtection"},
                                                {"label": "Tech Support", "value": "TechSupport"},
                                                {"label": "Streaming TV", "value": "StreamingTV"},
                                                {"label": "Streaming Movies", "value": "StreamingMovies"},
                                                {"label": "Contract", "value": "Contract"},
                                                {"label": "Paperless Billing", "value": "PaperlessBilling"},
                                                {"label": "Payment Method", "value": "PaymentMethod"},
                                                {"label": "Senior Citizen", "value": "SeniorCitizen"},
                            
                                            ], id = "categorical_dropdown", value="gender"
                                        )
                                    ]
                                ),


                                html.Img(src="../assets/customer.png", className="customer-img")
                                
                                
                                ],lg="4", sm=12,
                            ),


                            dbc.Col(card_donut, lg="4", sm=12),

                            # dbc.Spinner(id="loading2",size="md", color="light",children=[dbc.Col(card_categorical, lg="4", sm=12)]),

                            dbc.Col(card_categorical, lg="4", sm=12),

                        ], className="h-15", style={"height": "100%"}
                    )
                ]
            ),
            className="mt-3", style = {"background-color": "#272953"}
        ),

    # Tensure, MonthlyCharges and TotalCharges Visualizaion

    dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(card_tensure, lg="4", sm=12),
                        dbc.Col(card_monthlycharges, lg="4", sm=12),
                        dbc.Col(card_totalcharges, lg="4", sm=12),  
                    ], className="h-15"
                )
            ]
        ),
        className="mt-3", style = {"background-color": "#272953"}
    )

]

tab_analysis_content = tab_graphs


# PREDICTION

tab_prediction_features = dbc.Card(
    dbc.CardBody(
        [
            # First Row

            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Gender", addon_type="prepend"),
                                    dbc.Select(
                                        id="ft_gender",
                                        options=[
                                            {"label": "Female", "value": "Female"},
                                            {"label": "Male", "value": "Male"},
                                        ], value="Male"
                                    )
                                ]
                            )
                        ], lg="3", sm=12
                    ),
                    
                    #Age
                    
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Age(Yrs)", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_age",
                                        placeholder="Age", type="number", value="18"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),
                    
                    #dependent count
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Dependent Count(Number)", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_dependent_count",
                                        placeholder="Dependent Count", type="number", value="3"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),
                    
                    #Education_Level
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Education_Level", addon_type="prepend"),
                                    dbc.Select(
                                        id="ft_Education_Level",
                                        options=[
                                            {"label": "High School", "value": "High School"},
                                            {"label": "Graduate", "value": "Graduate"},
                                            {"label": "Uneducated", "value": "Uneducated"},
                                            {"label": "Uneducated", "value": "Uneducated"},
                                            {"label": "College", "value": "College"},
                                            {"label": "Post-Graduate", "value": "Post-Graduate"},
                                            {"label": "Doctorate", "value": "Doctorate"}
                                        ], value="Graduate"
                                    )
                                ]
                            )
                        ], lg="3", sm=12
                    ),
                ], className="feature-row",
            ), 

            # Second Row

            dbc.Row(
                [
                    # Marital Status

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Marital Status", addon_type="prepend"),
                                    dbc.Select(
                                        id="ft_Marital_Status",
                                        options=[
                                            {"label": "Married", "value": "Married"},
                                            {"label": "Single", "value": "Single"},
                                            {"label": "Unknown", "value": "Unknown"},
                                            {"label": "Divorced", "value": "Divorced"},
                                        ], value="Single"
                                    )
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # Income Category

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Income Category", addon_type="prepend"),
                                    dbc.Select(
                                        id="ft_income_category",
                                        options=[
                                            {"label": "Less than $40K", "value": "Less than $40K"},
                                            {"label": "$40K - $60K", "value": "$40K - $60K"},
                                            {"label": "$60K - $80K", "value": "$60K - $80K"},
                                            {"label": "$80K - $120K", "value": "$80K - $120K"},
                                            {"label": "$120K +", "value": "$120K +"},
                                            {"label": "Unknown", "value": "Unknown"},
                                        ], value="Less than $40K"
                                    )
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # Card_Category

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Card Category", addon_type="prepend"),
                                    dbc.Select(
                                        id="ft_Card_Category",
                                        options=[
                                            {"label": "Blue", "value": "Blue"},
                                            {"label": "Gold", "value": "Gold"},
                                            {"label": "Silver", "value": "Silver"},
                                            {"label": "Platinum", "value": "Platinum"},
                                        ], value="Blue"
                                    )
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # Months_on_book
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Months On Book(12-56)", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_months_on_book",
                                        placeholder="Months On Book(12-56(months))", type="number", value="13"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),
                    
                ], className="feature-row",
            ),

            # Third Row

            dbc.Row(
                [
                    # Total Relationship Count
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Relationship Count(1-5)", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_total_relationship_count",
                                        placeholder="Total Relationship Count(1-5)", type="number", value="1"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),
                    

                    # Months_Inactive_12_mon

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Months Inactive(0-12)", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_Months_Inactive",
                                        placeholder="Months Inactive(0-12)", type="number", value="1"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # Contacts_Count_12_mon

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Contacts Count(0-12)", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_Contact_Count",
                                        placeholder="Contacts Count(0-12)", type="number", value="1"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # Credit_Limit

                  dbc.Col(
                      [
                          dbc.InputGroup(
                              [
                                  dbc.InputGroupAddon("Credit Limit", addon_type="prepend"),
                                  dbc.Input(
                                      id="Credit_Limit",
                                      placeholder="Credit Limit(1K-35K)", type="number", value="1000"
                                  ),
                              ]
                          )
                      ], lg="3", sm=12
                  )  
                ], className="feature-row",
            ),

            # Fourth Row

            dbc.Row(
                [
                    # Total_Revolving_Bal

                     dbc.Col(
                         [
                             dbc.InputGroup(
                                 [
                                     dbc.InputGroupAddon("Tot Revolving Bal(0-2.6K)", addon_type="prepend"),
                                     dbc.Input(
                                         id="ft_Tot_Revolving_Balance",
                                         placeholder="Tot Revolving Bal(0-2.6K)", type="number", value="0"
                                     ),
                                 ]
                             )
                         ], lg="3", sm=12
                     ),


                    # Avg_Open_To_Buy
                    
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Avg Open to Buy(0-40K)", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_Avg_Open_to_Buy",
                                        placeholder="Avg Open to Buy(0-40K)", type="number", value="0"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),
                    


                    # Total_Amt_Chng_Q4_Q1
                    
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Tot Amt Chng(0.0-3.5)", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_Tot_Amt_Chng(0.0-3.5)",
                                        placeholder="Tot Amt Chng(0.0-3.5)", type="number", value="0.0"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),
                   

                    # Total Transaction Amt
                    
                   dbc.Col(
                       [
                           dbc.InputGroup(
                               [
                                   dbc.InputGroupAddon("Tot Trans Amt(500-20K)", addon_type="prepend"),
                                   dbc.Input(
                                       id="ft_Tot_Trans_Amt(500-20K)",
                                       placeholder="Tot Trans Amt(500-20K)", type="number", value="500"
                                   ),
                               ]
                           )
                       ], lg="3", sm=12
                   ),
                ], className="feature-row",
            ),

            # Fifth Row

            dbc.Row(
                [
                    # Total_Trans_Amt(Thousands)

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Tot_Trans_Amt(Thousands)", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_Tot_Trans_Amt",
                                        placeholder="Tot_Trans_Amt(Thousands)", type="number", value="510000"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # Total_Trans_Ct

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Tot Trans Ct(10-150)", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_tot_trans_ct",
                                        placeholder="Tot Trans Ct(10-150)", type="number", value="10"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),

                    # Total_Ct_Chng_Q4_Q1

                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Tot Ct Chng(0.0-4.0)", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_Tot_Ct_Chng",
                                        placeholder="Tot Ct Chng(0.0-4.0)", type="number", value="0.0"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),
                    
                    #Avg_Utilization_Ratio
                    dbc.Col(
                        [
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon("Avg Util Ratio(0.0-10.0)", addon_type="prepend"),
                                    dbc.Input(
                                        id="ft_Avg_Utilization_Ratio",
                                        placeholder="Avg Util Ratio(0.0-10.0)", type="number", value="0.0"
                                    ),
                                ]
                            )
                        ], lg="3", sm=12
                    ),
                    
                ], className="feature-row"
            ),
            
            #sixth row
            dbc.Row(
                [
                    # Geography
                      
                      dbc.Col(
                          [
                              dbc.InputGroup(
                                  [
                                      dbc.InputGroupAddon("Geography", addon_type="prepend"),
                                      dbc.Select(
                                          id="ft_Geography",
                                        options=[
                                            {"label": "Bangalore", "value": "Bangalore"},
                                            {"label": "Pune", "value": "Pune"},
                                            {"label": "Chennai", "value": "Chennai"},
                                            {"label": "Mumbai", "value": "Mumbai"},
                                            {"label": "Hyderabad", "value": "Hyderabad"},
                                            {"label": "Delhi", "value": "Delhi"},
                                        ], value="Delhi"
                                      )
                                  ]
                              )
                          ], lg="3", sm=12
                      ),

    
                ],
            ),
        ]
    ),
    className="mt-3", style = {"background-color": "#272953"}
)

tab_prediction_result = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Button("Predict", id='btn_predict', size="lg", className="btn-predict")
                        ], lg="4", sm=4, style={"display": "flex", "align-items":"center", "justify-content":"center"},
                        className="card-padding"
                    ),

                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Spinner(html.H4(id="xgb_result", children="-", style={'color':'#e7b328'}), size="sm", spinner_style={'margin-bottom': '5px'}),
                                        html.P("XGBoost")
                                    ]
                                ), className="result-card", style={"height":"16vh"}
                            )
                        ], lg=4, sm=4, className="card-padding"
                    ),

                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Spinner(html.H4(id="svm_result", children="-", style={'color':'#e7b328'}), size="sm", spinner_style={'margin-bottom': '5px'}),
                                        html.P("SVM")
                                    ]
                                ), className="result-card", style={"height":"16vh"}
                            )
                        ], lg=4, sm=4, className="card-padding"
                    )


                ]
            ),


        ]
    ),
    className="mt-3", style = {"background-color": "#272953"}
)

tab_prediction_content = [
    
    tab_prediction_features,
    tab_prediction_result
    
]