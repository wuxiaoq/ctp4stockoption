# -*- coding: utf-8 -*-
import soptthostmduserapi as mdapi  
import time

class CFtdcMdSpi(mdapi.CThostFtdcMdSpi):
    tapi=''
    def __init__(self,tapi):
        mdapi.CThostFtdcMdSpi.__init__(self)
        self.tapi=tapi
    def OnFrontConnected(self):
        print ("OnFrontConnected")
        loginfield = mdapi.CThostFtdcReqUserLoginField()
        loginfield.BrokerID="2001"
        loginfield.UserID="xxxxxxx"
        loginfield.Password="xxxxxx"
        loginfield.UserProductInfo="python dll"
        self.tapi.ReqUserLogin(loginfield,0)
    def OnRspUserLogin(self, *args):
        print ("OnRspUserLogin")
        rsploginfield=args[0]
        rspinfofield=args[1]
        print ("SessionID=",rsploginfield.SessionID)
        print ("ErrorID=",rspinfofield.ErrorID)
        print ("ErrorMsg=",rspinfofield.ErrorMsg)
        ret=self.tapi.SubscribeMarketData([b"90005726", b"90005724", b"90005719", ],3)

    def OnRtnDepthMarketData(self, *args):
        print ("OnRtnDepthMarketData")
        field=args[0]
        print ("InstrumentID=",field.InstrumentID, time.time())
        print ("LastPrice=",field.LastPrice , field.BidPrice1, field.AskPrice1)

    def OnRspSubMarketData(self, *args):
        print ("OnRspSubMarketData")
        field=args[0]
        print ("InstrumentID=",field.InstrumentID)
        rspinfofield=args[1]
        print ("ErrorID=",rspinfofield.ErrorID)
        print ("ErrorMsg=",rspinfofield.ErrorMsg)

def main():
    mduserapi=mdapi.CThostFtdcMdApi_CreateFtdcMdApi()
    mduserspi=CFtdcMdSpi(mduserapi) 
    mduserapi.RegisterFront("tcp://125.64.36.26:52219")
    mduserapi.RegisterSpi(mduserspi)
    mduserapi.Init()    
    mduserapi.Join()

if __name__ == '__main__':
    main()

