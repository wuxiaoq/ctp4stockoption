import time
import datetime
import soptthosttraderapi as api
import socket
import urllib.parse
from contextlib import closing
import logging
import json

FrontAddr="tcp://125.64.36.26:52207"
BROKERID="xxxx"

APPID = 'xxxx' 
AUTHCODE = 'xxxx' 

USERID="xxxx"
PASSWORD="xxxx"

product_info = 'MY SOFT'

EXCHANGEID="SZSE"
INSTRUMENTID="90005724"
PRICE=0.93
VOLUME=1

DIRECTION=api.THOST_FTDC_D_Sell

OFFSET="0" # open
# OFFSET="1" # close

orders = []

################################################################
# CTP连接测试
################################################################
def check_address_port(tcp):
    """
    :param tcp:
    :return:
    """
    host_schema = urllib.parse.urlparse(tcp)

    ip = host_schema.hostname
    port = host_schema.port
    print('trade server:',tcp)
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((ip, port)) == 0:
            return True  # OPEN
        else:
            return False  # closed


class CTradeSpi(api.CThostFtdcTraderSpi):
    
    tapi=''
    def __init__(self,tapi):
        api.CThostFtdcTraderSpi.__init__(self)
        self.tapi=tapi
        
    def OnFrontConnected(self) -> "void":
        print ("OnFrontConnected")
        # authfield = api.CThostFtdcReqAuthenticateField();
        # authfield.BrokerID=BROKERID
        # authfield.UserID=USERID
        # authfield.AppID=APPID
        # authfield.AuthCode=AUTHCODE
        # self.tapi.ReqAuthenticate(authfield,0)
        # print ("send ReqAuthenticate ok")
        
    def OnFrontDisconnected(self, intReason) -> "void":
        print ("OnFrontDisconnected", intReason)
        
        
    def OnRspAuthenticate(self, pRspAuthenticateField: 'CThostFtdcRspAuthenticateField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void": 
        print ("BrokerID=",pRspAuthenticateField.BrokerID)
        print ("AppID=",pRspAuthenticateField.AppID)
        print ("AppType=",pRspAuthenticateField.AppType)
        print ("ErrorID=",pRspInfo.ErrorID)
        print ("ErrorMsg=",pRspInfo.ErrorMsg)
        
        logging.info('认证OnRspAuthenticate:')
        logging.info('  BrokerID=%s', pRspAuthenticateField.BrokerID )
        logging.info('  AppID=%s', pRspAuthenticateField.AppID )
        logging.info('  ErrorID=%s', pRspInfo.ErrorID )
        logging.info('  ErrorMsg=%s', pRspInfo.ErrorMsg )
        # if not pRspInfo.ErrorID :
            # loginfield = api.CThostFtdcReqUserLoginField()
            # loginfield.BrokerID=BROKERID
            # loginfield.UserID=USERID
            # loginfield.Password=PASSWORD
            # loginfield.UserProductInfo="python dll"
            # self.tapi.ReqUserLogin(loginfield,0)
            # print ("send login ok")
    def OnRspUserLogout(self, pUserLogout: 'CThostFtdcUserLogoutField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
        print ("OnRspUserLogout")
        print ("ErrorID=",pRspInfo.ErrorID)
        print ("ErrorMsg=",pRspInfo.ErrorMsg)
        logging.info('登出: OnRspUserLogout')
        exit()
        
    def OnRspUserLogin(self, pRspUserLogin: 'CThostFtdcRspUserLoginField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
        print ("OnRspUserLogin")
        print ("UserID=",pRspUserLogin.UserID)
        print ("TradingDay=",pRspUserLogin.TradingDay)
        print ("SessionID=",pRspUserLogin.SessionID)
        print ("ErrorID=",pRspInfo.ErrorID)
        print ("ErrorMsg=",pRspInfo.ErrorMsg)
        
        logging.info('登录: OnRspUserLogin')
        logging.info('  TradingDay=%s', pRspUserLogin.TradingDay )
        logging.info('  SessionID=%s', pRspUserLogin.SessionID )
        logging.info('  ErrorID=%s', pRspInfo.ErrorID )
        logging.info('  ErrorMsg=%s', pRspInfo.ErrorMsg )

        qryinfofield = api.CThostFtdcQrySettlementInfoField()
        qryinfofield.BrokerID=BROKERID
        qryinfofield.InvestorID=USERID
        qryinfofield.TradingDay=pRspUserLogin.TradingDay
        self.tapi.ReqQrySettlementInfo(qryinfofield,0)
        print ("send ReqQrySettlementInfo ok")
        
    def OnRspQrySettlementInfo(self, pSettlementInfo: 'CThostFtdcSettlementInfoField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
        print ("OnRspQrySettlementInfo****")
        if  pSettlementInfo is not None :
            print ("content:",pSettlementInfo.Content)
        else :
            print ("content null")
        pSettlementInfoConfirm=api.CThostFtdcSettlementInfoConfirmField()
        pSettlementInfoConfirm.BrokerID=BROKERID
        pSettlementInfoConfirm.InvestorID=USERID
        self.tapi.ReqSettlementInfoConfirm(pSettlementInfoConfirm,0)
        print ("send ReqSettlementInfoConfirm ok")
        pass
        
    def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm: 'CThostFtdcSettlementInfoConfirmField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
        print ("OnRspSettlementInfoConfirm===")
        print ("ErrorID=",pRspInfo.ErrorID)
        print ("ErrorMsg=",pRspInfo.ErrorMsg)
        # ReqorderfieldInsert(self.tapi)
        # print ("send ReqorderfieldInsert ok")


    def OnRtnOrder(self, pOrder: 'CThostFtdcOrderField') -> "void":
        print ("OnRtnOrder")
        print ("OrderStatus=",pOrder.OrderStatus)
        print ("StatusMsg=",pOrder.StatusMsg)
        print ("LimitPrice=",pOrder.LimitPrice)
        print ("OrderSysID=",pOrder.OrderSysID)
        
        if '全部成交'==pOrder.StatusMsg:
            # 账号、日期、合约、开平标志、价格、数量
            logging.info('成交: UserID=%s 委托时间=%s 合约=%s 开平标志=%s 价格=%s 数量=%s ', pOrder.UserID, pOrder.InsertTime, pOrder.InstrumentID, pOrder.CombOffsetFlag, pOrder.LimitPrice, pOrder.VolumeTraded)
        elif '已撤单'==pOrder.StatusMsg:
            logging.info('撤单: UserID=%s 委托时间=%s 合约=%s 开平标志=%s 价格=%s 数量=%s 订单号=%s', pOrder.UserID, pOrder.InsertTime, pOrder.InstrumentID, pOrder.CombOffsetFlag, pOrder.LimitPrice, pOrder.VolumeTraded, pOrder.OrderSysID)
        elif '未成交'==pOrder.StatusMsg:
            
            logging.info('挂单: UserID=%s 委托时间=%s 合约=%s 开平标志=%s 价格=%s 数量=%s 订单号=%s', pOrder.UserID, pOrder.InsertTime, pOrder.InstrumentID, pOrder.CombOffsetFlag, pOrder.LimitPrice, pOrder.VolumeTraded, pOrder.OrderSysID)
                
    def OnRspOrderInsert(self, pInputOrder: 'CThostFtdcInputOrderField', pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool') -> "void":
        print ("OnRspOrderInsert")
        print ("ErrorID=",pRspInfo.ErrorID)
        print ("ErrorMsg=",pRspInfo.ErrorMsg)
        
##########################################################
# 撤单
##########################################################
def DelOrder(tdr, oid):
    inv=api.CThostFtdcInputOrderActionField()
    inv.BrokerID = BROKERID
    inv.InvestorID = USERID
    inv.ActionFlag = '0'
    inv.ExchangeID = EXCHANGEID 
    inv.OrderSysID = oid
    inv.RequestID = 0
    tdr.ReqOrderAction(inv, 0)

pre_time = 0
def ReqorderfieldInsert(tradeapi, p, vol=1, comboffset='0', direction=DIRECTION):
        
    print ("ReqOrderInsert Start")
    orderfield=api.CThostFtdcInputOrderField()
    orderfield.BrokerID=BROKERID
    orderfield.ExchangeID=EXCHANGEID
    orderfield.InstrumentID=INSTRUMENTID
    orderfield.UserID=USERID
    orderfield.InvestorID=USERID
    orderfield.Direction=direction
    orderfield.LimitPrice=p
    orderfield.VolumeTotalOriginal=VOLUME
    orderfield.OrderPriceType=api.THOST_FTDC_OPT_LimitPrice
    orderfield.ContingentCondition = api.THOST_FTDC_CC_Immediately
    orderfield.TimeCondition = api.THOST_FTDC_TC_GFD
    orderfield.VolumeCondition = api.THOST_FTDC_VC_AV
    orderfield.CombHedgeFlag="1"
    orderfield.CombOffsetFlag=comboffset
    orderfield.GTDDate=""
    orderfield.orderfieldRef="1"
    orderfield.MinVolume = 0
    orderfield.ForceCloseReason = api.THOST_FTDC_FCC_NotForceClose
    orderfield.IsAutoSuspend = 0
    tradeapi.ReqOrderInsert(orderfield,0)
    print ("ReqOrderInsert End")
        
def main():
    logging.info('股票期权测试启动' )
    print('股票期权测试启动\n')
    
    if check_address_port(FrontAddr):
        logging.info('服务器连接正常:%s', FrontAddr )
        print('服务器连接正常', FrontAddr)
    else:
        print("trader server down")
        exit()
        
    tradeapi=api.CThostFtdcTraderApi_CreateFtdcTraderApi()
    print(tradeapi.GetApiVersion(), tradeapi.GetTradingDay())
    
    tradespi=CTradeSpi(tradeapi)
    tradeapi.RegisterFront(FrontAddr)
    tradeapi.RegisterSpi(tradespi)
    tradeapi.SubscribePrivateTopic(api.THOST_TERT_QUICK)
    tradeapi.SubscribePublicTopic(api.THOST_TERT_QUICK)
    
    tradeapi.Init()
    
    time.sleep(1)
    
    print('认证参数', BROKERID, APPID, AUTHCODE, '\n')
    authreqfield = api.CThostFtdcReqAuthenticateField()
    authreqfield.BrokerID=BROKERID
    authreqfield.AuthCode=AUTHCODE
    authreqfield.AppID=APPID
    
    ret = tradeapi.ReqAuthenticate(authreqfield,1000)
        
    time.sleep(1)
    loginfield = api.CThostFtdcReqUserLoginField()
    loginfield.BrokerID=BROKERID
    loginfield.UserID=USERID
    loginfield.Password=PASSWORD
    loginfield.productinfo=product_info
    tradeapi.ReqUserLogin(loginfield,1230)
    
    
    time.sleep(2)
    
    
    ReqorderfieldInsert(tradeapi, 0.93)
    time.sleep(0.2)

            
    tradeapi.Join()
    
    
    
if __name__ == '__main__':
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='./log/ctp_trader_main.log', level=logging.INFO, format=LOG_FORMAT)
    main()