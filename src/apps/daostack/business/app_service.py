"""
   Descp: Manage the application logic, and it's used to interconect the
        data_access and presentation layers.

   Created on: 2-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List, Callable
import dash_html_components as html

from src.app import app
from src.apps.common.data_access.update_date import UpdateDate
import src.apps.common.presentation.dashboard_view.dashboard_view as view
import src.apps.common.presentation.dashboard_view.controller as view_cont
from src.apps.common.data_access.daos.organization_dao\
    import OrganizationListDao
import src.apps.daostack.data_access.daos.metric.\
    metric_dao_factory as s_factory
import src.apps.daostack.data_access.requesters.cache_requester as cache
from src.apps.common.business.transfers.organization import OrganizationList
from src.apps.common.business.singleton import Singleton
from src.apps.common.presentation.charts.chart_controller import ChartController
from src.apps.daostack.business.metric_adapter.metric_adapter import MetricAdapter
from src.apps.daostack.business.metric_adapter.proposal_boost_outcome \
    import ProposalBoostOutcome
from src.apps.daostack.business.metric_adapter.success_ratio_type \
    import SuccessRatioType
from src.apps.daostack.business.metric_adapter.vote_type \
    import VoteType
from src.apps.daostack.business.metric_adapter.majority_type \
    import MajorityType
from src.apps.common.presentation.charts.layout.chart_pane_layout \
    import ChartPaneLayout
from src.apps.common.presentation.charts.layout.figure.bar_figure import BarFigure
from src.apps.common.presentation.charts.layout.figure.multi_bar_figure \
    import MultiBarFigure
from src.apps.common.presentation.charts.layout.figure.double_scatter_figure \
    import DoubleScatterFigure
from src.apps.common.presentation.charts.layout.figure.figure import Figure
from src.apps.daostack.resources.strings import TEXT
from src.apps.common.resources.strings import TEXT as COMMON_TEXT

class DaostackService(metaclass=Singleton):
 
    _REP_H: int = 0
    _VOTE: int = 1
    _STAKE: int = 2
    _PROPOSAL: int = 3
    _ORGANIZATION: int = 4

    def __init__(self):
        # app state
        self.__orgs: OrganizationList = None
        self.__controllers: Dict[int, List[ChartController]] = {
            self._REP_H: list(),
            self._VOTE: list(),
            self._STAKE: list(),
            self._PROPOSAL: list(),
            self._ORGANIZATION: list(),
        }
        self.__already_bound: bool = False


    def bind_callbacks(self) -> None:
        if not self.__already_bound:
            self.__already_bound = True
            # Changing the DAO name if it changes
            view_cont.bind_callbacks(
                app=app,
                section_id=TEXT['css_id_organization'],
                organizations=self.organizations
            )
            self.__gen_sections()


    @property
    def organizations(self) -> OrganizationList:
        if not self.__orgs:
            orgs: OrganizationList = OrganizationListDao(cache.CacheRequester(
                srcs=[cache.DAOS])).get_organizations()
            if not orgs.is_empty():
                self.__orgs = orgs
                
        return self.__orgs


    @property
    def are_panes(self) -> bool:
        """
        Checks if panes and their controllers are already created.
        """
        return any(self.__controllers.values())


    def get_layout(self, org_value: str = None) -> html.Div:
        """
        Returns the app's layout. 
        """
        orgs: OrganizationList = self.organizations

        if not self.__already_bound:
            self.bind_callbacks()

        return view.generate_layout(
            labels=orgs.get_dict_representation(),
            sections=self.__get_sections(),
            ecosystem='daostack',
            update=UpdateDate().get_date(),
            org_value=org_value
        )

    def __gen_sections(self) -> None:
        self.__get_rep_holder_charts()
        self.__get_vote_charts()
        self.__get_stake_charts()
        self.__get_proposal_charts()
        self.__get_organization_charts()

    def __get_sections(self) -> Dict[str, List[Callable]]:
        """
        Returns a dict with each section filled with a callable function, which
         returns the chart layout.
        """
        l_rep_h: List[Callable] = list()
        l_vote: List[Callable] = list()
        l_stake: List[Callable] = list()
        l_proposal: List[Callable] = list()
        l_organization: List[Callable] = list()

        if not self.are_panes:
            self.__gen_sections()

        # Panes are already created.
        l_rep_h = [c.layout.get_layout for c in self.__controllers[self._REP_H]]
        l_vote = [c.layout.get_layout for c in self.__controllers[self._VOTE]]
        l_stake = [c.layout.get_layout for c in self.__controllers[self._STAKE]]
        l_proposal = [c.layout.get_layout for c in self.__controllers[self._PROPOSAL]]
        l_organization = [c.layout.get_layout for c in self.__controllers[self._ORGANIZATION]]

        return {
            COMMON_TEXT['no_data_selected']: {
                'callables': l_organization,
                'css_id': TEXT['css_id_organization'],
            },
            TEXT['rep_holder_title']: {
                'callables': l_rep_h,
                'css_id': TEXT['css_id_reputation_holders'],
            },
            TEXT['vote_title']: {
                'callables': l_vote,
                'css_id': TEXT['css_id_votes'],
            },
            TEXT['stake_title']: {
                'callables': l_stake,
                'css_id': TEXT['css_id_stake'],
            },
            TEXT['proposal_title']: {
                'callables': l_proposal,
                'css_id': TEXT['css_id_proposal'],
            },
        }


    def __get_organization_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # active organizations
        charts.append(self.__create_chart(
            title=TEXT['title_active_organization'],
            adapter=MetricAdapter(s_factory.ACTIVE_ORGANIZATION, call),
            figure=BarFigure(),
            cont_key=self._ORGANIZATION
        ))

        return charts


    def __get_rep_holder_charts(self) -> List[Callable[[], html.Div]]:
        """
        Creates charts of reputation holder section, this includes 
         its layout and its controller.
        """
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # new reputation holders
        charts.append(self.__create_chart(
            title=TEXT['new_users_title'],
            adapter=MetricAdapter(s_factory.NEW_USERS, call),
            figure=BarFigure(),
            cont_key=self._REP_H
        ))

        # total reputation holders
        charts.append(self.__create_chart(
            title=TEXT['total_users_title'],
            adapter=MetricAdapter(s_factory.TOTAL_REP_HOLDERS, call),
            figure=BarFigure(),
            cont_key=self._REP_H
        ))

        # active reputation holders
        charts.append(self.__create_chart(
            title=TEXT['active_users_title'],
            adapter=MetricAdapter(s_factory.ACTIVE_USERS, call),
            figure=BarFigure(),
            cont_key=self._REP_H
        ))
        return charts


    def __get_vote_charts(self) -> List[Callable[[], html.Div]]:
        """
        Creates charts of vote section.
        """
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # total votes by type
        charts.append(self.__create_chart(
            title=TEXT['total_votes_option_title'],
            adapter=VoteType(s_factory.TOTAL_VOTES_OPTION, call, VoteType.VOTE),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK),
            cont_key=self._VOTE
        ))

        # votes for rate
        charts.append(self.__create_chart(
            title=TEXT['vote_for_rate_title'],
            adapter=MetricAdapter(s_factory.VOTES_FOR_RATE, call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        self.__controllers[self._VOTE][-1].layout.configuration.disable_subtitles()

        # votes against rate
        charts.append(self.__create_chart(
            title=TEXT['vote_against_rate_title'],
            adapter=MetricAdapter(s_factory.VOTES_AGAINST_RATE, call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        self.__controllers[self._VOTE][-1].layout.configuration.disable_subtitles()

        # different voters
        charts.append(self.__create_chart(
            title=TEXT['different_voters_title'],
            adapter=MetricAdapter(s_factory.DIFFERENT_VOTERS, call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))

        # percentage of reputation holders which vote
        charts.append(self.__create_chart(
            title=TEXT['voters_percentage_title'],
            adapter=MetricAdapter(s_factory.VOTERS_PERCENTAGE, call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        self.__controllers[self._VOTE][-1].layout.configuration.disable_subtitles()
        self.__controllers[self._VOTE][-1].layout.figure\
            .configuration.add_y_params(params={
                'suffix': '%'})

        # vote-voters rate
        charts.append(self.__create_chart(
            title=TEXT['vote_voters_title'],
            adapter=MetricAdapter(s_factory.VOTE_VOTERS_RATE, call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))

        return charts


    def __get_stake_charts(self) -> List[Callable[[], html.Div]]:
        """
        Creates charts of stake section.
        """
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # total stakes
        charts.append(self.__create_chart(
            title=TEXT['total_stakes_title'],
            adapter=MetricAdapter(s_factory.TOTAL_STAKES, call),
            figure=BarFigure(),
            cont_key=self._STAKE
        ))
        # different stakers
        charts.append(self.__create_chart(
            title=TEXT['different_stakers_title'],
            adapter=MetricAdapter(s_factory.DIFFERENT_STAKERS, call),
            figure=BarFigure(),
            cont_key=self._STAKE
        ))
        return charts


    def __get_proposal_charts(self) -> List[Callable[[], html.Div]]:
        """
        Creates charts of proposal section.
        """
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # new proposals
        charts.append(self.__create_chart(
            title=TEXT['new_proposals_title'],
            adapter=MetricAdapter(s_factory.NEW_PROPOSALS, call),
            figure=BarFigure(),
            cont_key=self._PROPOSAL
        ))

        # majority type
        charts.append(self.__create_chart(
            title=TEXT['proposal_outcome_majority_title'],
            adapter=MajorityType(s_factory.PROPOSAL_MAJORITY, call),
            figure=DoubleScatterFigure(),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()

        # proposal boost_outcome
        charts.append(self.__create_chart(
            title=TEXT['proposal_boost_outcome_title'],
            adapter=ProposalBoostOutcome(s_factory.PROPOSALS_BOOST_OUTCOME, call),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()

        # proposal approve rate
        charts.append(self.__create_chart(
            title=TEXT['approval_proposal_rate_title'],
            adapter=MetricAdapter(s_factory.APPROVAL_PROPOSAL_RATE, call),
            figure=BarFigure(),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()

        # total succes rate of the stakes
        charts.append(self.__create_chart(
            title=TEXT['proposal_total_succ_rate_title'],
            adapter=MetricAdapter(s_factory.PROPOSALS_TOTAL_SUCCES_RATIO, call),
            figure=BarFigure(),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()

        # success rate by type
        charts.append(self.__create_chart(
            title=TEXT['proposal_boost_succ_rate_title'],
            adapter=SuccessRatioType(s_factory.PROPOSALS_BOOST_SUCCES_RATIO, call),
            figure=MultiBarFigure(bar_type=MultiBarFigure.GROUP),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()

        return charts


    def __create_chart(self, title: str, adapter: MetricAdapter, figure: Figure
    , cont_key: int) -> Callable:
        """
        Creates the chart layout and its controller, and returns a callable
        to get the html representation.
        """
        css_id: str = f"{TEXT['pane_css_prefix']}{ChartPaneLayout.pane_id()}"
        layout: ChartPaneLayout = ChartPaneLayout(
            title=title,
            css_id=css_id,
            figure=figure
        )
        layout.configuration.set_css_border(css_border=TEXT['css_pane_border'])

        controller: ChartController = ChartController(
            css_id=css_id,
            layout=layout,
            adapter=adapter)

        self.__controllers[cont_key].append(controller)
        return layout.get_layout
