import sqlite3, os, re
path = os.path.dirname(__file__)
from buy_2 import f
# 23_02_22_v01 수정본
# customer = [('번호','아이디','비번','이름','주소','이메일','적립금','총구매금액','회원등급')]
 
login_check = False

class Customer(f):

    # 회원가입 함수
    # 입력값 : 아이디, 비밀번호, 이름, 주소, 이메일
    # 1) DB에 중복되는 아이디가 있는지 확인
    # 2) 비밀번호 형태가 영문/숫자 8자리 이상인지 확인
    # 3) 이메일 형태가 @xxx.xxx맞는지 확인
    # 확인이 통과되면 입력받은 함수를 customer 테이블에 넣는다
    def signup_customer(self):
        conn = sqlite3.connect(path+'/mart.db')
        cur = conn.cursor()

        while 1: #DB에 입력된 아이디와 중복되지 않을떄까지 입력 반복
            cus_id = input('아이디 입력 >> ')
            check = 0
            for i in cur.execute('select * from customer'): #customer 테이블 반복
                if i[1] == cus_id:                          # i[1]은 테이블의 회원 아이디 값
                    check = 1
            if check == 0 :
                break
            print('중복되는 아이디가 있습니다.')

        while 1: #비밀번호를 영문,숫자 8자리 이상으로 입력할 때까지 반복
            cus_pw = input('비밀번호 입력 (영문,숫자 8자리 이상) >> ')
            pat = re.compile('[0-9a-zA-Z]{8,}')             # 정규표현식 : 영문 대소문자 or 숫자, 8자리 이상
            p = pat.match(cus_pw)
            if p != None:                                   # 매치값이 일치해서 데이터가 존재하면 통과
                break
            print('비밀번호 형태를 확인해 주세요.')      

        cus_name = input('이름 입력 >> ')
        cus_add = input('주소 입력 >> ')

        while 1: #이메일을 @xxx.xxx형태로 입력할 때까지 반복
            cus_email = input('이메일 입력 >> ')            
            pat = re.compile('@[a-z]*[.][a-z]*')            # 정규표현식 : @xxx.xxx
            p = pat.search(cus_email)
            if p != None:                                   # 매치값이 일치해서 데이터가 존재하면 통과
                break
            print('이메일 형식을 확인해 주세요. ex)hong@gmail.com')
        
        cus_save = 0
        cus_total = 0
        cus_grade = 'bronze'

        # 입력받은 값들을 customer 테이블에 넣음
        sql = 'insert into customer(cus_id, cus_pw, cus_name, cus_add, cus_email, cus_save, cus_total, cus_grade) values(?,?,?,?,?,?,?,?)'
        cur.execute(sql,(cus_id, cus_pw, cus_name, cus_add, cus_email, cus_save, cus_total, cus_grade))
        conn.commit()
        conn.close()

        # cus_num = 회원번호
        # cus_id = 회원아이디
        # cus_pw = 회원비밀번호
        # cus_name = 회원이름
        # cus_add = 회원주소
        # cus_email = 회원이메일
        # cus_save = 회원적립금 
        # cus_total = 회원총구매금액
        # cus_grade = 회원등급


    # 회원 로그인 함수
    # 입력값 : 회원아이디, 회원비밀번호
    # 로그인 함수에서 바뀌는 전역변수 login_check 값을 이용해서 True 값일때 아래 함수들인    
    # 회원정보조회, 회원정보수정, 회원탈퇴를 작동할 수 있게 한다
    def login_customer(self):

        conn = sqlite3.connect(path+'/mart.db')
        cur = conn.cursor()

        while 1:  # 일치하는 아이디를 입력할 때까지 반복
            cus_id = input('아이디 입력 (종료:Q)>> ')
            for i in cur.execute('select * from customer'):
                check = 0
                if i[1] == cus_id:                       # i[1]은 테이블의 회원 아이디 값
                    cus_pw = input('비밀번호 입력 >> ')
                    if i[2] == cus_pw:                  # i[2]은 테이블의 회원 비밀번호 값
                        check = 1
                        global login_check             
                        login_check = True              # 아이디/비밀번호가 DB값과 일치하면 전역변수 login_check를 True로 바꾼다
                        self.id = i[1]                  # self.id 인스턴스 변수를 입력한 아이디값으로 저장
                        print("로그인 성공!")
                        self.user_data = cur.execute(
                        f"""select cus_num,cus_grade,cus_save  
                                                    from customer
                                                    where cus_id='{cus_id}'
                                                    and cus_pw='{cus_pw}'"""
                        ).fetchone()                                # 로그인동시에 유저 데이터 가져옴
                        self.cus_id=cus_id
                        self.cus_pw=cus_pw
                        break
                    print('비밀번호가 일치하지 않습니다.')
            if cus_id in ('Q','q'):                     # 'Q','q'로 아이디 입력을 벗어남
                login_check = False
                break
            elif check == 1:                             # 제대로된 아이디/비밀번호 값을 받으면 반복을 벗어남
                break
            elif check == 0:                            # 아이디가 없을 경우 출력되고 아이디 입력으로 돌아간다
                print('존재하지 않는 아이디 입니다.')
        
        conn.close()
        return login_check

    def log_out(self):
        login_check = False
        self.id = ''
        return login_check

    
    # 회원 정보 조회 함수
    # 입력값 : x
    # 해당 아이디 회원정보를 출력
    # 로그인함수에서 입력받은 self.id(회원아이디)를 가져다 쓴다
    def view_customer(self):
        cus_id = self.id                                                # cus_id는 로그인함수에서 저장한 self.id를 가져옴

        conn = sqlite3.connect(path+'/mart.db')
        cur = conn.cursor()

        cur.execute(f"select * from customer where cus_id ='{cus_id}'") # customer테이블에서 cus_id와 일치하는 행을 가져옴
        item = cur.fetchone()
        
        if not item:
            print("사용자 정보가 없습니다.")
            return
        
        print(f'''
회원 번호   : {item[0]}
회원 아이디 : {item[1]}
회원 이름   : {item[3]}
회원 주소   : {item[4]}
회원 이메일 : {item[5]}
회원 적립금 : {item[6]}
총 구매금액 : {item[7]}
회원 등급   : {item[8]}
        ''')

        conn.close()



    # 회원 정보 수정 함수
    # 입력값 : 수정할 column
    # 해당 아이디 회원정보 열을 입력받아서 값을 업데이트
    # 로그인함수에서 입력받은 self.id(회원아이디)를 가져다 쓴다
    def update_customer(self):
        cus_id = self.id                                                # cus_id는 로그인함수에서 저장한 self.id를 가져옴

        conn = sqlite3.connect(path+'/mart.db')
        cur = conn.cursor()

        cur.execute(f"select * from customer where cus_id ='{cus_id}'") # customer테이블에서 cus_id와 일치하는 행을 가져옴
        item = cur.fetchone()
        print(f'''
회원 아이디 : {item[1]}
회원 이름   : {item[3]}
회원 주소   : {item[4]}
회원 이메일 : {item[5]}
        ''')                                                           # 간단한 회원정보를 출력해주고 수정할 내용을 입력받음
        key = input('''                                                 
============================
수정할 내용을 입력해 주세요.
1.비밀번호  2.주소  3.이메일
============================
>>>  ''')
        check = 0
        if key in ('1','비밀번호'):
            while 1: #비밀번호를 영문,숫자 8자리 이상으로 입력할 때까지 반복
                cus_pw = input('수정할 비밀번호 입력 (영문,숫자 8자리 이상) >>')
                pat = re.compile('[0-9a-zA-Z]{8,}')         # 정규표현식 : 영문 대소문자 or 숫자, 8자리 이상
                p = pat.match(cus_pw)               
                if p != None:                                # 매치값이 일치해서 데이터가 존재하면 통과
                    check=1
                    sql = f'update customer set cus_pw = ? where cus_id =? '   # 입력받은 비밀번호를 업데이트
                    cur.execute(sql,(cus_pw,cus_id))
                    break
                print('비밀번호 형태를 확인해 주세요.')
        elif key in ('2','주소'):
            cus_add = input('수정할 주소 입력 >>')
            check=1
            sql = f'update customer set cus_add = ? where cus_id =? '          # 입력받은 주소를 업데이트
            cur.execute(sql,(cus_add,cus_id))
        elif key in ('3','이메일'):
            while 1:
                cus_email = input('수정할 이메일 입력 >>')
                pat = re.compile('@[a-z]*[.][a-z]*')        # 정규표현식 : @xxx.xxx
                p = pat.search(cus_email)
                if p != None:                               # 매치값이 일치해서 데이터가 존재하면 통과
                    check=1
                    sql = f'update customer set cus_email = ? where cus_id =? ' # 입력받은 이메일를 업데이트
                    cur.execute(sql,(cus_email,cus_id))
                    break
                print('이메일 형식을 확인해 주세요. ex)hong@gmail.com')
        if check == 0 :                                     # 수정할 값 입력값을 잘못 입력했을때                               
            print('잘못 입력하셨습니다.')

        conn.commit()
        conn.close()


    # 회원탈퇴 함수
    # 입력값 : x
    # 해당 아이디 회원정보를 삭제
    # 로그인함수에서 입력받은 self.id(회원아이디)를 가져다 쓴다
    def withdraw_customer(self):
        cus_id = self.id                                             # cus_id는 로그인함수에서 저장한 self.id를 가져옴

        conn = sqlite3.connect(path+'/mart.db')
        cur = conn.cursor()

        cur.execute(f"delete from customer where cus_id ='{cus_id}'") # cus_id와 일치하는 행을 제거

        conn.commit()
        conn.close()


    # 사용자의 영수증 기록 다 출력 
    # 입력값 : X
    # 로그인함수에서 입력받은 self.id(회원아이디)를 가져다 쓴다
    # 회원아이디로 회원번호를 찾고 buy테이블에서 해당 회원의 데이터를 가져다 쓴다
    def buy_log_print(self):
        conn = sqlite3.connect(path+'/mart.db')
        cur = conn.cursor()
        u=cur.execute(f"""select * from buy 
                                    where cus_num=(select cus_num from customer
                                                        where cus_id='{self.id}')""").fetchall()
        for i in u :   # cus_id는 로그인함수에서 저장한 self.id를 가져옴
            #i=self.cur.execute("select * from buy order by buy_date").fetchall()[-1]
            ww=cur.execute(f"select mat_name from materiel_management where mat_index={i[1]} ").fetchone()[0]   #물품명은 buy테이블에 없어서 m-m테이블에서 가져옴
            id1 = cur.execute(f"select cus_id from customer where cus_num = {i[2]} ").fetchone()[0] # 영수증 사용자 id를 customer 테이블에서 cus_id를 찾아서 가져옴
            print(f"영수증 번호 : {i[0]} ")
            print(f"사용자 ID   : {id1} ")
            print(f"사용자 등급 : {i[3]} ")
            print(f"물품 명     : {ww} ")
            print(f"구매 개수   : {i[5]} ")
            print(f"구매 지점   : {i[4]} ")
            print(f"구매 총액   : {i[6]} ")
            print(f"구매 시간   : {i[-1]} \n")

        self.back_buy(u)
        save_money = cur.execute(f"select cus_save from customer where cus_id='{self.id}'").fetchone()[0]
        if save_money < 0:
            cur.execute(f"update customer set cus_save = 0 where cus_id = '{self.id}'" )
    # 환불하는함수 
    def back_buy(self,u):
        #선택
        a=input("환불할 영수증 번호를 선택하세요. 종료 (q)")
        if not a.isdecimal():
            print("숫자를 입력하세요 ")
            return
        a=int(a)

        # 내역에 있는값인지 확인 
        ck=1
        for i in u:
            if i[0] == a:
                index=i[1]
                price1=i[6]
                count=i[5]
                dis=i[7]
                discount=i[8]
                u_s=i[10]
                ck=0
                break
            
        # 없거나 이미 환불한내역 
        if ck==1:
            print("없는번호")
        elif price1<0:
            print("환불내역입니다.")
   
        else:
            for j in u:
                if (i[1],i[2],j[4],-i[5],-i[6],i[7])==(j[1],j[2],j[4],j[5],j[6],j[7]):
                    print("이미 환불한 내역입니다")
                    return

            # 아니면 이제 값 가져아서 환불 함 
            item_name,item_price=self.cur.execute(f"""select mat_name,mat_price from materiel_management
                                        where mat_index='{index}'""").fetchone()

            user_save=-((item_price * count - item_price * count * discount / 100) if dis  else item_price * count)-price1

            count=-i[5]
            price1=-i[6]
            self.buy_update(item_name,item_price,user_save, dis,
                               discount, index, count,price1)

    # 로그인 하지 않고 회원 정보 조회하는 함수
    # 입력값 : 회원아이디
    # 로그인 하지 않고 회원아이디만 입력후 정보 출력
    def info_customer(self):
        conn = sqlite3.connect(path+'/mart.db')
        cur = conn.cursor()

        cus_id = input('아이디 입력 >> ')
        check = 0
        for i in cur.execute('select * from customer'):
            if i[1] == cus_id:                                                  # i[1]은 테이블의 회원 아이디 값
                cur.execute(f"select * from customer where cus_id ='{cus_id}'") # customer테이블에서 cus_id와 일치하는 행을 가져옴
                item = cur.fetchone()
                print(f'''
회원 번호   : {item[0]}
회원 아이디 : {item[1]}
회원 이름   : {item[3]}
회원 적립금 : {item[6]}
총 구매금액 : {item[7]}
회원 등급   : {item[8]}''')
                check = 1
                break
        if check == 0:
            print('일치하는 회원정보가 없습니다.')
                    
        conn.close()


# a = Customer()
# # a.signup_customer()
# a.login_customer()
# # a.view_customer()
# # a.update_customer()
# # a.withdraw_customer()
# # a.info_customer()
# a.buy_log_print()


 
        
        

        
