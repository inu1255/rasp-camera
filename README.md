# 树莓派运动检测监控

1. 运动检测自动拍照+录像
2. 通过qqbot通知指定qq
3. baidupcs将照片上传到百度云

**适用于raspbian系统**

## 安装

添加国内源  
``` bash
# vim /etc/apt/source.list
deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi
deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi
```

安装opencv,numpy,pip
``` bash
apt-get install python-opencv python-pip python-dev python-numpy
```

加载摄像头模块
``` bash
modprobe bcm2835-v4l2
# ls /dev/video0 
# 显示 /dev/video0 则成功
```

安装qqbot
``` bash
pip install qqbot
```
配置方法见[qqbot](https://github.com/pandolia/qqbot/)

clone本项目并运行
``` bash
git clone https://github.com/inu1255/rasp-camera.git
cd rasp-camera
python main.py
```

## 上传百度云

需要automake
``` bash
apt-get install automake
```
[编译安装见](https://github.com/GangZhuo/BaiduPCS)

开始同步,u上传,r递归子目录
``` bash
baidupcs synch -ru /path/to/rasp-camera/images /path/to/baidu/pan
```

通过crontab定时备份