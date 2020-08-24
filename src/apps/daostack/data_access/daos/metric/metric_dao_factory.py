"""
   Descp: A factory of dao stacked serie

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
from typing import List

from src.apps.daostack.data_access.daos.metric.metric_dao \
    import MetricDao
import src.apps.daostack.data_access.requesters.cache_requester as cache
import src.apps.daostack.data_access.daos.metric.strategy.\
    st_time_serie as st_s
import src.apps.daostack.data_access.daos.metric.strategy.\
    st_proposal_outcome as st_po
import src.apps.daostack.data_access.daos.metric.strategy.\
    st_different_voters_stakers as st_vs
from src.apps.daostack.data_access.daos.metric.strategy.\
    st_proposal_majority import StProposalMajority
import src.apps.daostack.data_access.daos.metric.strategy.\
    st_total_votes_stakes_option as st_tvso
from src.apps.daostack.data_access.daos.metric.strategy.st_active_users\
    import StActiveUsers

NEW_USERS = 0
NEW_PROPOSALS = 1
PROPOSALS_BOOST_OUTCOME = 2
TOTAL_VOTES = 3
TOTAL_STAKES = 4
DIFFERENT_VOTERS = 5
DIFFERENT_STAKERS = 6
PROPOSAL_MAJORITY = 7
PROPOSALS_TOTAL_SUCCES_RATIO = 8
PROPOSALS_BOOST_SUCCES_RATIO = 9
TOTAL_VOTES_OPTION = 10
TOTAL_STAKES_OPTION = 11
ACTIVE_USERS = 12


def get_dao(ids: List[str], metric: int) -> MetricDao: # noqa: C901
    requester: cache.CacheRequester = None
    stg = None
    
    if metric == NEW_USERS:
        stg = st_s.StTimeSerie(st_s.NEW_USERS)
        requester = cache.CacheRequester(srcs=[cache.REP_HOLDERS])
    elif metric == NEW_PROPOSALS:
        stg = st_s.StTimeSerie(st_s.NEW_PROPOSAL)
        requester = cache.CacheRequester(srcs=[cache.PROPOSALS])
    elif metric == TOTAL_VOTES:
        stg = st_s.StTimeSerie(st_s.TOTAL_VOTES)
        requester = cache.CacheRequester(srcs=[cache.VOTES])
    elif metric == TOTAL_STAKES:
        stg = st_s.StTimeSerie(st_s.TOTAL_STAKES)
        requester = cache.CacheRequester(srcs=[cache.STAKES])
    elif metric == PROPOSALS_BOOST_OUTCOME:
        stg = st_po.StProposalOutcome(st_po.BOOST_OUTCOME)
        requester = cache.CacheRequester(srcs=[cache.PROPOSALS])
    elif metric == DIFFERENT_VOTERS:
        stg = st_vs.StDifferentVS(st_vs.VOTERS)
        requester = cache.CacheRequester(srcs=[cache.VOTES])
    elif metric == DIFFERENT_STAKERS:
        stg = st_vs.StDifferentVS(st_vs.STAKERS)
        requester = cache.CacheRequester(srcs=[cache.STAKES])
    elif metric == PROPOSAL_MAJORITY:
        stg = StProposalMajority()
        requester = cache.CacheRequester(srcs=[cache.PROPOSALS])
    elif metric == PROPOSALS_TOTAL_SUCCES_RATIO:
        stg = st_po.StProposalOutcome(st_po.TOTAL_SUCCESS_RATIO)
        requester = cache.CacheRequester(srcs=[cache.PROPOSALS])
    elif metric == PROPOSALS_BOOST_SUCCES_RATIO:
        stg = st_po.StProposalOutcome(st_po.BOOST_SUCCESS_RATIO)
        requester = cache.CacheRequester(srcs=[cache.PROPOSALS])
    elif metric == TOTAL_VOTES_OPTION:
        stg = st_tvso.StTotalVSOption(st_tvso.VOTES)
        requester = cache.CacheRequester(srcs=[cache.VOTES])
    elif metric == TOTAL_STAKES_OPTION:
        stg = st_tvso.StTotalVSOption(st_tvso.STAKES)
        requester = cache.CacheRequester(srcs=[cache.STAKES])
    elif metric == ACTIVE_USERS:
        stg = StActiveUsers()
        requester = cache.CacheRequester(srcs=[
            cache.PROPOSALS, 
            cache.VOTES, 
            cache.STAKES])

    return MetricDao(ids=ids, strategy=stg, requester=requester)
