import random
from pyunit_prime import get_large_prime_length    #随机生成指定长度大素数
from pyunit_prime import is_prime                  #判断素数
from pyunit_prime import prime_range               #输出指定区间素数
import math
import time

#记录时间
start = time.perf_counter() #记下开始时刻


p=0
q=0
    
def primeFactorization(length):                    #分解质因数
    global p,q
    q=get_large_prime_length(length)
    while True:
        d=random.randint(2,10000)
        if d%2==0:
            p=q*d+1
            if is_prime(p)==True:
                break
            else:
                continue
        else:
            continue
    primeList=prime_range(2,int(math.sqrt(d)))
    result=[[0,0] for i in range(len(primeList))]
    for i in range(len(primeList)):
        result[i][0]=primeList[i]
        while d%primeList[i]==0:
            result[i][1]+=1
            d=d//primeList[i]
    if d!=1:
        result.append([d,1])
    result.append([q,1])
    return result  

def quickPower(a,b,c):                               #快速幂
    result=1
    while b>0:
        if b%2==1:
            result=result*a%c
        a=a*a%c
        b>>=1
    return result

def getGenerator(result):                             #get g
    generator=random.randint(1,1000)
    while True:
        if quickPower(generator,q,p)!=1:
            generator+=1
        else:
            for i in range(len(result)):
                if quickPower(generator,int((p-1)/result[i][0]),p)==1:
                    break
            if i!=len(result)-1:
                generator+=1
            else:
                break
    return generator

def getSecretKey():                                 #get SK,x
    x=random.randint(1,q)
    return x

def getPublicKey(g,x):                             #get PK,h
    h=quickPower(g,x,p)
    return h

def treatMSG(msg):                                #处理消息msg为整数
    newmsg=''
    for i in msg:
        newmsg+=str(ord(i))
    return int(newmsg)

def ChameleonHash(PK,g,m,r,I):                       #变色龙哈希
    g1 = g*I                    #变色龙哈希
    CH=quickPower(g1,m,p)*quickPower(PK,r,p)%p
    return CH

def ChameleonHash2(ya,g,m,p,I):                       #变色龙哈希
    g1 = g*I                       #变色龙哈希
    CH=quickPower(g1,m,p)* ya %p
    return CH

def exgcd(a,b):                                    #扩展欧几里得
    if b==0:
        return 1,0,a
    else:
        x,y,gcd=exgcd(b,a%b)
        x,y=y,(x-(a//b)*y)
        return x,y,gcd

def Forge(SK,m1,r1,m2,g,p,I):                            #求y^a`
    #x,y,gcd=exgcd(SK,q)
    temp1 = SK*r1
    temp2 = m1-m2
    g1 = g*I
    result=quickPower(g,temp1,p)*quickPower(g1,temp2,p)%p
    return result

if __name__ == "__main__":
    print('calculating...')
    print('')
    length=100                                    #随机大素数长度
    result=primeFactorization(length)
    g=getGenerator(result)
    SK=getSecretKey()
    PK=getPublicKey(g,SK)
    
    I = 3113112002004132010030030032150010010001110102312002003113112014132034052032012012003112003102004006216124004015024014014018354017234004004007321276101979612511912015715115218417718020419720021420721022021321633242722121321422421621721921121122721921922121321321520720721220420471636319141330222217116316320019219321921121222922122222421621763525423222122322321221422721721723021821823121921722521321122421221061535395878711710910991120319219421620520722521421623422122374616323221821923321922023522122223622121923922422224523022823121621457484579706711911010715014113817552061941942192072072332192201281141152412252262452292302412262242482302292472292282402222212432252244637346455529384811251161131581461461422206722821421515413813924623023124823022925023223125223223124722722624222222124122122037282546373471625910394911271151131591471455239371520171156154234219217240222221246228227248228227239219218233213212237217216332421463734453633736461102939012611411216215014818917617419518218023522021822921421222620820722921121023822021922821020922921121025171728202044363654464674666699898912811811816715515516915715725524624718617317120018518320619118921319819621620119922320820612762621202924234035345247467567679890901069898131121121161151151201189187164152150179167165194182180193180178205192190834171213272223312627423837514645696463736867948686115107107139131131156148148149139139171161161171161161181171171200200200200421200510400510400500721500500721500001213000000000111200311200200501400501612400400001001000000111000000000310200422311200311200200

    msg1='i sent first message and it must be long enough'                  #消息1
    msg2='this is for message sdfsdfsfs'                        #消息2
    newmsg1=treatMSG(msg1)
    newmsg2=treatMSG(msg2)
    rand1=random.randint(1,q)                    # r

    print('q=',q)
    print('p=',p)
    print('g=',g)
    print('SK=',SK)
    print('PK=',PK)
    print('')

    print('msg1=',msg1)
    print('rand1=',rand1)
    CH=ChameleonHash(PK,g,newmsg1,rand1,I)
    print('CH=',CH)
    print('')
    
    print('msg2=',msg2)
    rand2=Forge(SK,newmsg1,rand1,newmsg2,g,p,I)
    #rand2=Forge(SK,newmsg1,rand1,newmsg2)
    print('rand2=',rand2)
    newCH=ChameleonHash2(rand2,g,newmsg2,p,I)
    #newCH=ChameleonHash(PK,g,newmsg2,rand2)
    print('newCH=',newCH)



'''此处写需要计时的代码段'''
#time.sleep(1) #这行代码作用是停顿6秒钟
'''以上是需要计时的代码段'''
end = time.perf_counter()   #记下结束时刻
print ("\n程序用时为：" , end - start, 's')


print(len(str(newCH)))