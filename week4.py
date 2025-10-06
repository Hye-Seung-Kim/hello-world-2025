from PIL import Image, ImageDraw, ImageFilter
import tkinter as tk
import random

# 기획 : Mark Rothko Picture Motive
# 설정
canvasWidth = 600
canvasHeight = 800
scaleFactor = 4

# 고해상도 이미지 생성
myImage = Image.new("RGBA", (canvasWidth * scaleFactor, canvasHeight * scaleFactor), (255, 255, 255, 255))
drawingContext = ImageDraw.Draw(myImage, "RGBA")

# 배경색 (파란색)
background_color = (70, 110, 160, 255)
drawingContext.rectangle([(0, 0), (canvasWidth * scaleFactor, canvasHeight * scaleFactor)], fill=background_color)

# 붓 터치 효과를 주는 사각형 그리기 함수
def drawBrushRectangle(x, y, width, height, color, alpha=255):
    # 여러 겹의 약간씩 다른 사각형을 그려서 붓터치 효과
    for i in range(15):
        offset_x = random.randint(-8, 8)
        offset_y = random.randint(-8, 8)
        size_variation = random.randint(-10, 10)
        
        x0 = (x + offset_x) * scaleFactor
        y0 = (y + offset_y) * scaleFactor
        x1 = (x + width + offset_x + size_variation) * scaleFactor
        y1 = (y + height + offset_y + size_variation) * scaleFactor
        
        current_alpha = alpha + random.randint(-30, 30)
        current_alpha = max(0, min(255, current_alpha))
        
        current_color = tuple(max(0, min(255, c + random.randint(-5, 5))) for c in color)
        
        drawingContext.rectangle([(x0, y0), (x1, y1)], fill=(*current_color, current_alpha))

# 가장자리 블러 효과를 주는 함수
def drawSoftEdgeRectangle(x, y, width, height, color, edge_blur=20):
    # 중심부 (불투명)
    drawBrushRectangle(x + edge_blur, y + edge_blur, width - edge_blur * 2, height - edge_blur * 2, color, alpha=220)
    
    # 가장자리 그라디언트 레이어
    for i in range(edge_blur):
        alpha = int(220 * (1 - i / edge_blur))
        drawBrushRectangle(x + i, y + i, width - i * 2, height - i * 2, color, alpha=alpha)

# 상단 아이보리/베이지 띠 (뿌옇게)
drawSoftEdgeRectangle(20, 10, canvasWidth - 40, 60, (230, 220, 200), edge_blur=15)

# 중앙 큰 노란색 사각형 (선명하게)
drawSoftEdgeRectangle(30, 120, canvasWidth - 60, 320, (240, 200, 70), edge_blur=25)

# 하단 아이보리/연한 베이지 사각형 (뿌옇게)
drawSoftEdgeRectangle(30, 480, canvasWidth - 60, 280, (225, 215, 195), edge_blur=25)

# 이미지 다운샘플링
myImage = myImage.resize((canvasWidth, canvasHeight), Image.LANCZOS)

# 블러 효과를 여러 번 적용 (붓터치 느낌)
myImage = myImage.filter(ImageFilter.GaussianBlur(radius=12))
myImage = myImage.filter(ImageFilter.GaussianBlur(radius=6))
myImage = myImage.filter(ImageFilter.GaussianBlur(radius=3))

# 약간의 텍스처 추가
texture_layer = Image.new("RGBA", (canvasWidth, canvasHeight), (0, 0, 0, 0))
texture_draw = ImageDraw.Draw(texture_layer, "RGBA")

for i in range(5000):
    x = random.randint(0, canvasWidth)
    y = random.randint(0, canvasHeight)
    size = random.randint(1, 3)
    alpha = random.randint(5, 20)
    color = random.choice([(255, 255, 255, alpha), (0, 0, 0, alpha)])
    texture_draw.ellipse((x, y, x + size, y + size), fill=color)

myImage = Image.alpha_composite(myImage.convert("RGBA"), texture_layer)

# 이미지 저장
myImage.save("rothko-style-pattern.png", bitmap_format="png")
print("이미지가 'rothko-style-pattern.png'로 저장되었습니다!")

# Tkinter 윈도우에 표시
from PIL import ImageTk
window = tk.Tk()
window.title("로스코 스타일 추상화")
imageTk = ImageTk.PhotoImage(myImage)
tk.Label(window, image=imageTk).pack()
window.mainloop()