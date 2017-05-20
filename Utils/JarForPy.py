# coding=utf-8
from jpype import *

class JarForPy(object):
    def getjarrult_static(self, jarpath, packageclass, defname, *defparams):
        #startJVM(getDefaultJVMPath(), '-ea', "-Djava.class.path=%s" % 'e_pay.jar;JarForPython-0.0.1-SNAPSHOT.jar')
        #JavaClass = JClass("com.jartest.JarForPython.App")
        startJVM(getDefaultJVMPath(), '-ea', "-Djava.class.path=%s" % jarpath)
        JavaClass = JClass(packageclass)
        rult = ''
        if hasattr(JavaClass, defname):
            func = getattr(JavaClass,defname)
            rult = func(*defparams)
        else:
            rult = defname + ' not found!'
        shutdownJVM()
        return rult

    def getjarrult_normal(self, jarpath, packageclass, defname, *defparams):
        startJVM(getDefaultJVMPath(), '-ea', "-Djava.class.path=%s" % jarpath)
        JavaClass = JClass(packageclass)
        newJavaClass = JavaClass()
        rult = ''
        if hasattr(newJavaClass, defname):
            func = getattr(newJavaClass, defname)
            rult = func(defparams)
        else:
            rult = defname + ' not found!'
        shutdownJVM()
        return rult

    def testtest(self,*t):
        print len(t)
        for tt in t:
            print tt
if __name__ =='__main__':
    test = JarForPy()
    #print  test.getjarrult_static('JarForPython-0.0.1-SNAPSHOT.jar','com.jartest.JarForPython.App','jarforpy','Jacky','Wower go!')

    testpara = 'Jacky,Wower go!'.split(',')
    test.testtest(*testpara)
    #testpara = tuple('Jacky,Wower go!'.split(','))
    print  test.getjarrult_static('JarForPython-0.0.1-SNAPSHOT.jar', 'com.jartest.JarForPython.App', 'jarforpy',*testpara)