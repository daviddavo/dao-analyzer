"""
   Descp: It's used to create the dashboard view.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from apps.dashboard.resources.strings import TEXT

DARK_BLUE = '#2471a3'
LIGHT_BLUE = '#d4e6f1'
DARK_RED = '#F44336'
LIGHT_RED = '#EF9A9A'
DARK_GREEN = '#4CAF50'
LIGHT_GREEN = '#A5D6A7'

def generate_layout(labels: List[Dict[str, str]]) -> html.Div:
    """
    Use this function to generate the app view.
    Params:
        labels: A list of dictionaries for each element, in order to 
        fill the dropdown selector.
    Return:
        A html.Div filled with the app view 
    """
    return html.Div(
        children = [
            html.Div(
                children = [
                    __generate_header(),
                ],
                className = 'main-header'
            ),

            html.Div(
                children = [
                    __generate_dao_selector(labels),
                    __generate_all_graphs(),
                ],
                className = 'main-body'
            ),

            html.Div(
                children = [],
                className = 'main-foot'
            ),
        ],
        className = 'root',
    )


def __generate_header() -> html.H2:
    return html.H1(TEXT['app_title'])
    

def __generate_dao_selector(labels: List[Dict[str, str]]) -> html.Div:
    return html.Div( 
        children = [
            html.Span(TEXT['dao_selector_title']),
            dcc.Dropdown(
                id = 'org-dropdown',
                options = labels,
                className = 'drop-down'
            )
        ],
        className = 'pane dao-selector-pane',
    )


def __generate_all_graphs() -> html.Div:
    return html.Div(
        children = [
            __generate_graph(
                figure_gen = generate_bar_chart,
                css_id = 'new-users',
                title = TEXT['new_users_title'],
                amount = TEXT['default_amount'],
                subtitle = TEXT['no_data_selected'],
            ),
            __generate_graph(
                figure_gen = generate_bar_chart,
                css_id = 'new-proposal',
                title = TEXT['new_proposals_title'],
                amount = TEXT['default_amount'],
                subtitle = TEXT['no_data_selected'],
            ),
            __generate_graph(
                figure_gen = generate_4stacked_bar_chart,
                css_id = 'proposals-type',
                title = TEXT['proposal_type_title'],
            ),
        ],
        className = 'graphs-container',
    )


def __generate_graph(figure_gen, css_id: str, title: str, amount: str = None,
    subtitle: str = None) -> html.Div:

    children: List = [html.H3(title)]
    if amount:
        children.append(html.H2(amount, id = f'{css_id}-amount'))
    if subtitle:
        children.append(html.Span(subtitle, id = f'{css_id}-subtitle'))

    children.append( dcc.Graph( id = f'{css_id}-graph', figure = figure_gen()))

    return html.Div(children = children, className = 'pane graph-pane')


def generate_bar_chart(x: List = None, y: List = None) -> Dict:
    if not x:
        x = list()
    
    if not y:
        y = list()

    color = LIGHT_BLUE
    if x:
        color = [LIGHT_BLUE] * len(x)
        color[-1] = DARK_BLUE

    return {
        'data': [{
            'x': x,
            'y': y,
            'type': 'bar',
            'marker': { 'color': color }
        }],
        'layout': {
            'xaxis': {
                #'range': [data['x'][0], data['x'][-1]],
                'ticks':'outside',
                'tick0': 0,
                'ticklen': 8,
                'tickwidth': 2
                },
        }
    }


def generate_4stacked_bar_chart(x: List = None, y: List[List] = None) -> Dict:
    data: List = list()
    #p_range: List = [0, 1] 
    if x and y:
        bar1: go.Bar = go.Bar(x=x, y=y[0], name=TEXT['abs_fail'], marker_color=DARK_RED)
        bar2: go.Bar = go.Bar(x=x, y=y[1], name=TEXT['abs_pass'], marker_color=DARK_GREEN)
        bar3: go.Bar = go.Bar(x=x, y=y[2], name=TEXT['rel_fail'], marker_color=LIGHT_RED)
        bar4: go.Bar = go.Bar(x=x, y=y[3], name=TEXT['rel_pass'], marker_color=LIGHT_GREEN)
        data = [bar2, bar4, bar3, bar1]
        #p_range = [x[0], x[-1]]

    layout: go.Layout = go.Layout(barmode = 'stack', xaxis = {
                                                        'ticks':'outside',
                                                        'tick0': 0,
                                                        'ticklen': 8,
                                                        'tickwidth': 2,
                                                        #'range': p_range,
                                                    })
    return {'data': data, 'layout': layout}