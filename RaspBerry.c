#include<stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>

#define SERVER_PORT 8888
#define BUFF_LEN 1024
int main(int argc,char *argv[])
{
    int server_fd,ret;
    struct sockaddr_in ser_addr;//套接字地址结构体

    server_fd=socket(AF_INET, SOCK_DGRAM ,0); //AF_INET:IPV4; SOCK_DGRAM:UDP
    if(server_fd<0)
    {
        printf("create socket fail!\n");
        return -1;
    }
    
    memset(&ser_addr, 0 , sizeof(ser_addr));//清空该套接子的结构体
    ser_addr.sin_family=AF_INET;
    ser_addr.sin_addr.s_addr=htonl(INADDR_ANY);//IP地址，需要进行网络序转换，INADDR_ANY：本地地址
    ser_addr.sin_port=htons(SERVER_PORT);//端口号，需要网络序转换,上面定义的8888

    ret=bind(server_fd,(struct sockaddr*)&ser_addr, sizeof(ser_addr ));
    if(ret<0)
    {
        printf("socket bind fail!\n");
        return -1;
    }

    //接收和发送
    char buf[BUFF_LEN];//接收缓冲区，1024字节
    socklen_t len;
    int count;
    struct sockaddr_in clent_addr;//clent_addr用于记录发送方的地址信息
    while (1)
    {
        memset(buf,0,BUFF_LEN);//将缓冲区清空
        len=sizeof(clent_addr);
        count=recvfrom(server_fd,buf,BUFF_LEN,0,(struct sockaddr*)&clent_addr,&len);//recvfrom是拥塞函数，没有数据就一直拥塞
        if(count==-1)
        {
            printf("recieve data fail!\n");
            return;
        }
        else
        {
            printf("%s",buf);
            FILE *fp=NULL;
            char data[100]={'0'};//用来存储返回的cpu温度
            fp=popen("vcgencmd measure_temp","r");//以popen的方式打开
            if(fp==NULL)
            {
                printf("popen error!\n");
                return 1;
            }
            fgets(data,sizeof(data),fp);
            sendto(server_fd,data,sizeof(data),0,(struct sockaddr*)&clent_addr,len);//将温度发送过去
            
            pclose(fp);// 关闭文件
        }
    }
    
    return 0;
}