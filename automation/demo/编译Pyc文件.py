# -.- coding:utf-8 -.-
import compileall

compile_dir = raw_input(u"输入要遍历的文件夹路径:")

compileall.compile_dir(compile_dir)

print "编译成功，路径为%s" % compile_dir
