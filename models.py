from extensions import db, Column

class Customer(db.Model):
    __tablename__ = 'customer'

    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(100), unique=True, nullable=False)
    password = Column(db.String(100), nullable=False)
    personal_token = Column(db.String(100), unique=True, nullable=False)
    dropped = Column(db.Boolean, default=False)

#class Subscription(db.Model):
#    __tablename__ = 'subscription'
#
#    id = Column(db.Integer, primary_key=True)
#    name = Column(db.String(100), nullable=False)

#class CustomerSubscription(db.Model):
#    __tablename__ = 'customer_subscription'
#
#    id = Column(db.Integer, primary_key=True)
#    customer_id = Column(db.Integer, ForeignKey('customer.id'), nullable=False)
#    subscription_id = Column(db.Integer, ForeignKey('subscription.id'), nullable=False)
#    is_active = Column(db.Boolean, nullable=False, default=True)

#    customer = relationship('Customer', backref='subscriptions')
#    subscription = relationship('Subscription', backref='customers')