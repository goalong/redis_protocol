### 按照redis protocol对命令返回值进行解析

共分为五种类型，每种类型以第一个字节作为标识

简单字符串、整数、错误回复都比较简单清晰，就是除第一个字节之外的部分，然后去除末尾的\r\n;

批量字符串稍微复杂一点，不过也很好办；

比较复杂的是数组类型的，是一个可以综合的包含所有这五个类型的结构，实现上我是按\r\n将字符串
分隔开，组成一个列表，然后从左往右依次处理列表中每一项，每一项根据它的首个字符来确定使用的解码函数，
需要注意的点是一些特殊的情况，比如空的字符串，空的列表，None，对这些要单独处理。
