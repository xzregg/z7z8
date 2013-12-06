#coding:utf-8

#依赖倒置


#抽象类
class ICAR(object):
    def run(self):pass
    def trun(self):pass
    def stop(self):pass


#具体类
class HondaCar(ICAR):

    def __get__(self,instance,owner):
        print '__get__'
    def __getattribute__(self, item):
        print '__getattribute__%s' % item
        return item
    def run(self):
        print '本田run'
    def trun(self):
        print '本田trun'
    def stop(self):
        print '本田stop'

    def __getattr__(self, name):
        print '__getattr__%s'% name
#抽象类
class AutoSystem(object):
    carobj = HondaCar()
    def __init__(self):
        self.carobj = HondaCar()
    def runcar(self):
        self.carobj.run()
    def truncar(self):
        self.carobj.trun()
    def stopcar(self):
        self.carobj.stop()

if __name__ == "__main__":
    hodacar = HondaCar()
    #auto = AutoSystem()
    #auto.runcar()
    #auto.truncar()
    hodacar.run()


#总结：依赖倒置原则
#A.高层次的模块不应该依赖于低层次的模块，他们都应该依赖于抽象。
#B.抽象不应该依赖于具体，具体应该依赖于抽象。