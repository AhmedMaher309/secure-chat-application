# ctf 3

# step 1
simpley added both of the images using opencv

code:
```python
import cv2

image1 = cv2.imread('first.png')
image2 = cv2.imread('second.png')

cv2.imwrite("flag.png", image1+image2)
```

run the code 
```
python main.py
```

the flag will be in flag.png
