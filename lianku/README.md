oepnfire开发
==============

1.openfire安装配置过程中的数据库URL要这样填写：
jdbc:mysql://127.0.0.1:3306/linkcube?rewriteBatchedStatements=true&useUnicode=true&characterEncoding=utf8
而且mysql数据库中的字符也应选用utf8_gnenral_ci，否则离线消息会出现乱码

2.该项目导入eclipse中编译，请参考说明文档：编译运行openfire源码.docx

3.插件开发时使用ant方式编译，请参考说明文档：openfire插件开发.docx
另外，编译openfire也可以使用ant方式，只要在target中选中openfire即可。