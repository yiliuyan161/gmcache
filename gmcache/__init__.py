# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals

import getopt
import hashlib
import pickle
import sys
from functools import wraps
from os.path import expanduser

from diskcache import Cache
from gm import __version__
from gm.csdk.c_sdk import py_gmi_set_version
from gm.enum import *
from gm.model.storage import Context

home = expanduser("~").replace("\\", "/")
cache = Cache(directory=home + "/.gmcache", timeout=60, sqlite_synchronous=0)

# 基本api
from gm.api.basic import (
    set_token, set_mfp, get_version, subscribe, unsubscribe,
    current, get_strerror, schedule, run, set_parameter,
    add_parameter, log, set_serv_addr, stop)

# 两融api
from gm.api.credit import credit_get_borrowable_instruments_positions, credit_buying_on_collateral, \
    credit_repay_cash_by_selling_share, credit_get_cash, credit_buying_on_margin, credit_get_borrowable_instruments, \
    credit_get_collateral_instruments, credit_get_contracts, credit_repay_cash_directly, \
    credit_repay_share_by_buying_share, credit_repay_share_directly, credit_selling_on_collateral, credit_short_selling, \
    credit_collateral_in, credit_collateral_out

# IPO新股
from gm.api.ipo import ipo_buy, ipo_get_quota, ipo_get_lot_info, ipo_get_instruments, ipo_get_match_number

# 基金
from gm.api.fund import fund_buy, fund_etf_buy, fund_redemption, fund_subscribing, fund_etf_redemption

# 债券(含可转债)
from gm.api.bond import bond_reverse_repurchase_agreement, bond_convertible_put, bond_convertible_call, \
    bond_convertible_put_cancel

# 数据查询api
from gm.api import query


def _compute_key(args, kwargs):
    """
    计算缓存key
    :param args:
    :param kwargs:
    :return:
    """
    key = []
    if args and len(args) > 0:
        for arg in args:
            if isinstance(arg, type({}.keys())) or isinstance(arg, list):
                arg = tuple(arg)
                key += arg
            elif isinstance(arg, dict):
                arg = tuple(arg.items())
                key += arg
            else:
                key.append(arg)
    if kwargs:
        for item in sorted(kwargs.items()):
            k = item[0]
            v = item[1]
            if isinstance(v, type({}.keys())):
                v = tuple(v)
            elif isinstance(v, dict):
                v = tuple(v.items())
            elif isinstance(v, list):
                v = tuple(v)
            key += (k, v)
    key = pickle.dumps(tuple(key))
    return hashlib.sha1(key).hexdigest()


def clear_cache():
    """
    清理全部缓存
    :return:
    """
    cache.clear()


def gm_cache(expire=604800):
    """
    缓存API调用返回的结果
    """

    def _memoize(function):
        @wraps(function)  # 自动复制函数信息
        def __memoize(*args, **kwargs):
            key = "gm_" + function.__module__ + "." + function.__qualname__ + "|" + _compute_key(
                args, kwargs)
            with cache:
                cached = cache.get(key)
            if cached is None:
                cached = function(*args, **kwargs)
                with cache:
                    cache.set(key, cached, expire=expire)
            return cached

        return __memoize

    return _memoize


@gm_cache()
def history_n(*args, **kwargs):
    return query.history_n(*args, **kwargs)


@gm_cache()
def history(*args, **kwargs):
    return query.history(*args, **kwargs)


@gm_cache()
def get_fundamentals(*args, **kwargs):
    return query.get_fundamentals(*args, **kwargs)


@gm_cache()
def get_dividend(*args, **kwargs):
    return query.get_dividend(*args, **kwargs)


@gm_cache()
def get_continuous_contracts(*args, **kwargs):
    return query.get_continuous_contracts(*args, **kwargs)


@gm_cache()
def get_next_trading_date(*args, **kwargs):
    return query.get_next_trading_date(*args, **kwargs)


@gm_cache()
def get_previous_trading_date(*args, **kwargs):
    return query.get_previous_trading_date(*args, **kwargs)


@gm_cache()
def get_trading_dates(*args, **kwargs):
    return query.get_trading_dates(*args, **kwargs)


@gm_cache()
def get_concept(*args, **kwargs):
    return query.get_concept(*args, **kwargs)


@gm_cache()
def get_industry(*args, **kwargs):
    return query.get_industry(*args, **kwargs)


@gm_cache()
def get_constituents(*args, **kwargs):
    return query.get_constituents(*args, **kwargs)


@gm_cache()
def get_history_constituents(*args, **kwargs):
    return query.get_history_constituents(*args, **kwargs)


@gm_cache()
def get_history_instruments(*args, **kwargs):
    return query.get_history_instruments(*args, **kwargs)


@gm_cache()
def get_instrumentinfos(*args, **kwargs):
    return query.get_instrumentinfos(*args, **kwargs)


@gm_cache()
def get_instruments(*args, **kwargs):
    return query.get_instruments(*args, **kwargs)


@gm_cache()
def get_sector(*args, **kwargs):
    return query.get_sector(*args, **kwargs)


@gm_cache()
def get_fundamentals_n(*args, **kwargs):
    return query.get_fundamentals_n(*args, **kwargs)


@gm_cache()
def get_history_l2ticks(*args, **kwargs):
    return query.get_history_l2ticks(*args, **kwargs)


@gm_cache()
def get_history_ticks_l2(*args, **kwargs):
    return query.get_history_ticks_l2(*args, **kwargs)


@gm_cache()
def get_history_l2bars(*args, **kwargs):
    return query.get_history_l2bars(*args, **kwargs)


@gm_cache()
def get_history_bars_l2(*args, **kwargs):
    return query.get_history_bars_l2(*args, **kwargs)


@gm_cache()
def get_history_l2transactions(*args, **kwargs):
    return query.get_history_l2transactions(*args, **kwargs)


@gm_cache()
def get_history_transaction_l2(*args, **kwargs):
    return query.get_history_transaction_l2(*args, **kwargs)


@gm_cache()
def get_history_l2orders(*args, **kwargs):
    return query.get_history_l2orders(*args, **kwargs)


@gm_cache()
def get_history_l2orders_queue(*args, **kwargs):
    return query.get_history_l2orders_queue(*args, **kwargs)


@gm_cache()
def raw_func(*args, **kwargs):
    return query.raw_func(*args, **kwargs)


# 交易api
from gm.api.trade import (
    order_target_volume, order_target_value, order_target_percent,
    order_volume, order_percent, order_value, order_batch,
    order_cancel_all, order_cancel, order_close_all,
    get_orders, get_unfinished_orders, get_execution_reports,
    algo_order, algo_order_cancel, algo_order_pause, get_algo_orders, get_algo_child_orders
)

__all__ = [
    'order_target_volume', 'order_target_value', 'order_target_percent',
    'order_volume', 'order_percent', 'order_value', 'order_batch',
    'order_cancel_all', 'order_cancel', 'order_close_all',
    'get_orders', 'get_unfinished_orders', 'get_execution_reports',
    'algo_order', 'algo_order_cancel', 'algo_order_pause', 'get_algo_orders', 'get_algo_child_orders',

    'set_token', 'set_mfp', 'get_version', 'subscribe', 'unsubscribe',
    'current', 'get_strerror', 'schedule', 'run',
    'set_parameter', 'add_parameter', 'log', 'stop',

    'history_n', 'history', 'get_fundamentals', 'get_dividend',
    'get_continuous_contracts', 'get_next_trading_date',
    'get_previous_trading_date', 'get_trading_dates', 'get_concept',
    'get_industry', 'get_constituents', 'get_history_constituents',
    'get_history_instruments', 'get_instrumentinfos', 'get_fundamentals_n',
    'get_instruments', 'get_sector', 'set_serv_addr', 'get_history_l2ticks', 'get_history_ticks_l2',
    'get_history_l2bars', 'get_history_bars_l2', 'raw_func',
    'get_history_l2transactions', 'get_history_transaction_l2', 'get_history_l2orders', 'get_history_l2orders_queue',

    'credit_get_borrowable_instruments_positions', 'credit_buying_on_collateral',
    'credit_repay_cash_by_selling_share', 'credit_get_cash', 'credit_buying_on_margin',
    'credit_get_borrowable_instruments',
    'credit_get_collateral_instruments', 'credit_get_contracts', 'credit_repay_cash_directly',
    'credit_repay_share_by_buying_share', 'credit_repay_share_directly', 'credit_selling_on_collateral',
    'credit_short_selling', 'credit_collateral_in', 'credit_collateral_out',

    'ipo_buy', 'ipo_get_quota', 'ipo_get_lot_info', 'ipo_get_instruments', 'ipo_get_match_number',

    'fund_buy', 'fund_etf_redemption', 'fund_subscribing', 'fund_redemption', 'fund_etf_buy',

    'bond_reverse_repurchase_agreement', 'bond_convertible_put', 'bond_convertible_call', 'bond_convertible_put_cancel',

    'Context',

    'ExecType_Unknown',
    'ExecType_New',
    'ExecType_DoneForDay',
    'ExecType_Canceled',
    'ExecType_PendingCancel',
    'ExecType_Stopped',
    'ExecType_Rejected',
    'ExecType_Suspended',
    'ExecType_PendingNew',
    'ExecType_Calculated',
    'ExecType_Expired',
    'ExecType_Restated',
    'ExecType_PendingReplace',
    'ExecType_Trade',
    'ExecType_TradeCorrect',
    'ExecType_TradeCancel',
    'ExecType_OrderStatus',
    'ExecType_CancelRejected',
    'OrderStatus_Unknown',
    'OrderStatus_New',
    'OrderStatus_PartiallyFilled',
    'OrderStatus_Filled',
    'OrderStatus_DoneForDay',
    'OrderStatus_Canceled',
    'OrderStatus_PendingCancel',
    'OrderStatus_Stopped',
    'OrderStatus_Rejected',
    'OrderStatus_Suspended',
    'OrderStatus_PendingNew',
    'OrderStatus_Calculated',
    'OrderStatus_Expired',
    'OrderStatus_AcceptedForBidding',
    'OrderStatus_PendingReplace',
    'OrderRejectReason_Unknown',
    'OrderRejectReason_RiskRuleCheckFailed',
    'OrderRejectReason_NoEnoughCash',
    'OrderRejectReason_NoEnoughPosition',
    'OrderRejectReason_IllegalAccountId',
    'OrderRejectReason_IllegalStrategyId',
    'OrderRejectReason_IllegalSymbol',
    'OrderRejectReason_IllegalVolume',
    'OrderRejectReason_IllegalPrice',
    'OrderRejectReason_AccountDisabled',
    'OrderRejectReason_AccountDisconnected',
    'OrderRejectReason_AccountLoggedout',
    'OrderRejectReason_NotInTradingSession',
    'OrderRejectReason_OrderTypeNotSupported',
    'OrderRejectReason_Throttle',
    'CancelOrderRejectReason_OrderFinalized',
    'CancelOrderRejectReason_UnknownOrder',
    'CancelOrderRejectReason_BrokerOption',
    'CancelOrderRejectReason_AlreadyInPendingCancel',
    'OrderSide_Unknown',
    'OrderSide_Buy',
    'OrderSide_Sell',
    'OrderType_Unknown',
    'OrderType_Limit',
    'OrderType_Market',
    'OrderType_Stop',
    'OrderDuration_Unknown',
    'OrderDuration_FAK',
    'OrderDuration_FOK',
    'OrderDuration_GFD',
    'OrderDuration_GFS',
    'OrderDuration_GTD',
    'OrderDuration_GTC',
    'OrderDuration_GFA',
    'OrderDuration_AHT',
    'OrderQualifier_Unknown',
    'OrderQualifier_BOC',
    'OrderQualifier_BOP',
    'OrderQualifier_B5TC',
    'OrderQualifier_B5TL',
    'OrderStyle_Unknown',
    'OrderStyle_Volume',
    'OrderStyle_Value',
    'OrderStyle_Percent',
    'OrderStyle_TargetVolume',
    'OrderStyle_TargetValue',
    'OrderStyle_TargetPercent',
    'PositionSide_Unknown',
    'PositionSide_Long',
    'PositionSide_Short',
    'PositionEffect_Unknown',
    'PositionEffect_Open',
    'PositionEffect_Close',
    'PositionEffect_CloseToday',
    'PositionEffect_CloseYesterday',
    'CashPositionChangeReason_Unknown',
    'CashPositionChangeReason_Trade',
    'CashPositionChangeReason_Inout',
    'MODE_LIVE',
    'MODE_BACKTEST',
    'ADJUST_NONE',
    'ADJUST_PREV',
    'ADJUST_POST',
    'SEC_TYPE_STOCK',
    'SEC_TYPE_FUND',
    'SEC_TYPE_INDEX',
    'SEC_TYPE_FUTURE',
    'SEC_TYPE_OPTION',
    'SEC_TYPE_CONFUTURE',
    'SEC_TYPE_BOND',
    'SEC_TYPE_BOND_CONVERTIBLE',
    'PositionSrc_Unknown',
    'PositionSrc_L1',
    'PositionSrc_L2',

    'OrderBusiness_NORMAL',
    'OrderBusiness_STOCK_BUY',
    'OrderBusiness_STOCK_SELL',
    'OrderBusiness_FUTURE_BUY_OPEN',
    'OrderBusiness_FUTURE_SELL_CLOSE',
    'OrderBusiness_FUTURE_SELL_CLOSE_TODAY',
    'OrderBusiness_FUTURE_SELL_CLOSE_YESTERDAY',
    'OrderBusiness_FUTURE_SELL_OPEN',
    'OrderBusiness_FUTURE_BUY_CLOSE',
    'OrderBusiness_FUTURE_BUY_CLOSE_TODAY',
    'OrderBusiness_FUTURE_BUY_CLOSE_YESTERDAY',
    'OrderBusiness_IPO_BUY',
    'OrderBusiness_CREDIT_BOM',
    'OrderBusiness_CREDIT_SS',
    'OrderBusiness_CREDIT_RSBBS',
    'OrderBusiness_CREDIT_RCBSS',
    'OrderBusiness_CREDIT_DRS',
    'OrderBusiness_CREDIT_DRC',
    'OrderBusiness_CREDIT_CPOM',
    'OrderBusiness_CREDIT_CPOSS',
    'OrderBusiness_CREDIT_BOC',
    'OrderBusiness_CREDIT_SOC',
    'OrderBusiness_CREDIT_CI',
    'OrderBusiness_CREDIT_CO',
    'OrderBusiness_CREDIT_BOM_VIP',
    'OrderBusiness_CREDIT_SS_VIP',
    'OrderBusiness_CREDIT_RSBBS_VIP',
    'OrderBusiness_CREDIT_RCBSS_VIP',
    'OrderBusiness_CREDIT_DRS_VIP',
    'OrderBusiness_CREDIT_DRC_VIP',
    'OrderBusiness_ETF_BUY',
    'OrderBusiness_ETF_RED',
    'OrderBusiness_FUND_SUB',
    'OrderBusiness_FUND_BUY',
    'OrderBusiness_FUND_RED',
    'OrderBusiness_FUND_CONVERT',
    'OrderBusiness_FUND_SPLIT',
    'OrderBusiness_FUND_MERGE',
    'OrderBusiness_BOND_RRP',
    'OrderBusiness_BOND_CONVERTIBLE_BUY',
    'OrderBusiness_BOND_CONVERTIBLE_CALL',
    'OrderBusiness_BOND_CONVERTIBLE_PUT',
    'OrderBusiness_BOND_CONVERTIBLE_PUT_CANCEL',

    'AlgoOrderStatus_Unknown', 'AlgoOrderStatus_Resume', 'AlgoOrderStatus_Pause',
    'AlgoOrderStatus_PauseAndCancelSubOrders',
    'clear_cache'
]

try:
    if sys.version_info.major < 3:
        __all__ = [str(item) for item in __all__]
    ver_info = sys.version_info
    sdk_lang = "python{}.{}".format(ver_info.major, ver_info.minor)
    sdk_version = __version__.__version__

    py_gmi_set_version(sdk_version, sdk_lang)

    command_argv = sys.argv[1:]
    options, console_args = getopt.getopt(command_argv, None,
                                          ['strategy_id=', 'filename=',
                                           'mode=', 'token=', 'apitoken=',
                                           'backtest_start_time=',
                                           'backtest_end_time=',
                                           'backtest_initial_cash=',
                                           'backtest_transaction_ratio=',
                                           'backtest_commission_ratio=',
                                           'backtest_slippage_ratio=',
                                           'backtest_adjust=',
                                           'backtest_check_cache=',
                                           'serv_addr=',
                                           'port=',  # 用于pycharm的python console时会额外传入port参数
                                           ])

    for option, value in options:
        if option == '--serv_addr' and value:
            set_serv_addr(value)
            break
except BaseException as e:
    pass
