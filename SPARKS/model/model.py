from sqlalchemy import *
from sqlalchemy.sql import *
engine=create_engine('mysql+pymysql://root:admin@127.0.0.1:3306/banking',echo=True)

class First:
    def __init__(self):
        self.meta=MetaData()
        self.customer=Table("customer",self.meta,autoload=True,autoload_with=engine)
        self.history=Table("history",self.meta,autoload=True,autoload_with=engine)
    
    def get_customers(self):
        s=self.customer.select()
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results
        else:
            return None

    def get_history(self):
        s=self.history.select()
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results
        else:
            return None
    
    def check_and_transfer(self,data):
        id=data['id']
        sacc=data['sacc']
        sname=data['sname']
        racc=data['racc']
        rname=data['rname']
        amt=data['amt']
        sender=self.customer.select().where(and_(
            self.customer.c.Account_No==sacc,
            self.customer.c.Customer_Name==sname
            ))
        send=engine.execute(sender)
        result1=[dict(r) for r in send] if send else 0
        receiver=self.customer.select().where(and_(
            self.customer.c.Account_No==racc,
            self.customer.c.Customer_Name==rname
            ))
        receive=engine.execute(receiver)
        result2=[dict(r) for r in receive] if receive else 0
        if result1 and result2:
            hist=engine.execute(self.history.insert().values(TransactionId=id,SenderAcc=sacc,SenderName=sname,ReceiverAcc=racc,ReceiverName=rname,Amount=amt))
            
            s=engine.execute(self.customer.update().where(self.customer.c.Account_No==sacc).values(Amount=self.customer.c.Amount-amt))
            r=engine.execute(self.customer.update().where(self.customer.c.Account_No==racc).values(Amount=self.customer.c.Amount+amt))
            if hist and s and r:                
                return 1
        else:
            return 0


    def transfer_money(self,data):
        id=data['id']
        sacc=data['sacc']
        sname=data['sname']
        racc=data['racc']
        rname=data['rname']
        amt=data['amt']
        sender=self.customer.select().where(and_(
            self.customer.c.Account_No==sacc,
            self.customer.c.Customer_Name==sname
            ))
        send=engine.execute(sender)
        result1=[dict(r) for r in send] if send else 0
        receiver=self.customer.select().where(and_(
            self.customer.c.Account_No==racc,
            self.customer.c.Customer_Name==rname
            ))
        receive=engine.execute(receiver)
        result2=[dict(r) for r in receive] if receive else 0
        if result1 and result2:
            hist=engine.execute(self.history.insert().values(TransactionId=id,SenderAcc=sacc,SenderName=sname,ReceiverAcc=racc,ReceiverName=rname,Amount=amt))
            if hist:
                return 1
        else:
            return 0
