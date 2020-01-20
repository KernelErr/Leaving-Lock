# Leaving-Lock
这是一个基于面部识别的程序，当计算机在10秒内检测不到它的Owner在看屏幕的时候就会自动锁屏（原生仅支持Windows，您可以自行修改）。

## 使用说明
- 首先安装好依赖：
	1. cmake
	2. scikit-image
	3. dlib
	4. face_recognition
	5. numpy
	6. opencv-python
- 然后运行`Register.py`，当有且仅有一张脸被检测到之后，程序会在接下来的30s内保存数百个特征向量组，请在这个时间内录入脸部的多个角度（就是让你疯狂转头）。
- 之后你可以运行`Recognition_Test.py`看看能否识别出你为Owner。
- 最后跑主程序即可。

## 程序原理
我们使用的是face_recognition库，而实际上face_recognition是对dlib的一个调用。我们首先从摄像头中获取到人脸位置，然后将人脸转换为128维特征向量，并保存下来。之后仅需要对比新向量与保存的向量的距离即可判断面部相似程度。

我们发现直接模拟按下`win + L`无法休眠计算机，于是调用了dll：`rundll32.exe user32.dll LockWorkStation`。

## 写在最后
1. 本程序希望能够给大家对于面部识别多一点启发。
2. 作者的conda环境内安装了大量包，可能缺失依赖，请提issue。
3. 欢迎任何疑问和建议。