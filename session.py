import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Sale, Shop, Stock

login = 'postgres'
password = ''

DSN = f'postgresql://{login}:{password}@localhost:5432/book_shop'
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

p_1 = Publisher(name='Александр Сергеевич Пушкин')
sh_1 = Shop(name='Буквоед')
sh_2 = Shop(name='Лабиринт')
sh_3 = Shop(name='Книжный дом')
b_1 = Book(title='Капитанская дочка', publishers=p_1)
b_2 = Book(title='Руслан и Людмила', publishers=p_1)
b_3 = Book(title='Евгений Онегин', publishers=p_1)
st_1 = Stock(books=b_1, shops=sh_1, count=150)
st_2 = Stock(books=b_2, shops=sh_1, count=100)
st_3 = Stock(books=b_1, shops=sh_2, count=98)
st_4 = Stock(books=b_3, shops=sh_3, count=50)
sale_1 = Sale(price=600, date_sale='09-11-2022', stocks=st_1, count=3)
sale_2 = Sale(price=500, date_sale='08-11-2022', stocks=st_2, count=2)
sale_3 = Sale(price=580, date_sale='05-11-2022', stocks=st_3, count=2)
sale_4 = Sale(price=490, date_sale='02-11-2022', stocks=st_4, count=3)
sale_5 = Sale(price=600, date_sale='26-10-2022', stocks=st_1, count=3)

session.add_all([p_1, sh_1, sh_2, sh_3, b_1, b_2, b_3, st_1, st_2, st_3,
                 st_4, sale_1, sale_2, sale_3, sale_4, sale_5])
session.commit()


def find_sale(publisher_name=None, shop_name=None):
    if publisher_name is not None and shop_name is None:
        for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Sale.stocks).join(Stock.shops) \
                .join(Stock.books).join(Book.publishers).filter(Publisher.name.like(f'%{publisher_name}%')):
            print(c)
    elif publisher_name is None and shop_name is not None:
        for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Sale.stocks).join(Stock.shops) \
                .join(Stock.books).join(Book.publishers).filter(Shop.name.like(f'%{shop_name}%')):
            print(c)
    elif publisher_name is not None and shop_name is not None:
        for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Sale.stocks).join(Stock.shops) \
                .join(Stock.books).join(Book.publishers).filter(Shop.name.like(f'%{shop_name}%'),
                                                                Publisher.name.like(f'%{publisher_name}%')):
            print(c)


session.close()

if __name__ == "__main__":
    # find_sale(publisher_name='Пушк')
    # find_sale(shop_name='Букв')
    find_sale(publisher_name='Пушк', shop_name='Кни')