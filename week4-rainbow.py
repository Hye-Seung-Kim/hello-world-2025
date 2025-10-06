from PIL import Image, ImageDraw, ImageTk, ImageFilter
import tkinter as tk
import seaborn as sns

# 기획 : 마크 로스코(Mark Rothko) 느낌의 그림으로 만들어보기
# 설정
canvasWidth = 800
canvasHeight = 800
scaleFactor = 4
gridRows = 12
gridCols = 12

# 무지개 색상 팔레트 생성 (Spectral 또는 rainbow)
palette = list(sns.color_palette("Spectral", gridRows * gridCols).as_hex())

# RGB로 변환
get_rgb = lambda x: list(int(x[i : i + 2], 16) for i in (0, 2, 4))
new_palette = [elem.replace("#", "") for elem in palette]
rgb_palette = list(map(get_rgb, new_palette))

# 고해상도 이미지 생성 (RGBA 모드로 변경)
myImage = Image.new("RGBA", (canvasWidth * scaleFactor, canvasHeight * scaleFactor), (255, 255, 255, 255))
drawingContext = ImageDraw.Draw(myImage, "RGBA")

# 원 그리기 함수 (투명도 지원)
def drawCircle(x, y, radius, color, alpha=255):
    x0 = (x - radius) * scaleFactor
    y0 = (y - radius) * scaleFactor
    x1 = (x + radius) * scaleFactor
    y1 = (y + radius) * scaleFactor
    color_with_alpha = (*color, alpha)
    drawingContext.ellipse((x0, y0, x1, y1), fill=color_with_alpha)

# 그리드 크기 계산
cellWidth = canvasWidth / gridCols
cellHeight = canvasHeight / gridRows

# 그리드에 원 그리기 (여러 레이어로)
import random
color_index = 0
for i in range(gridRows):
    for j in range(gridCols):
        # 각 셀의 중심점 계산
        x = cellWidth * j + cellWidth / 2
        y = cellHeight * i + cellHeight / 2
        
        # 원의 반지름 (셀 크기의 60% - 더 크게)
        radius = min(cellWidth, cellHeight) * 0.6
        
        # 무지개 색상 적용
        color = rgb_palette[color_index]
        
        # 여러 겹으로 그려서 블러 효과
        drawCircle(x, y, radius * 1.2, color, alpha=100)
        drawCircle(x, y, radius * 0.8, color, alpha=150)
        drawCircle(x, y, radius * 0.5, color, alpha=200)
        
        color_index += 1

# 이미지 다운샘플링 (안티앨리어싱)
myImage = myImage.resize((canvasWidth, canvasHeight), Image.LANCZOS)

# 블러 효과 적용 (여러 번 적용)
myImage = myImage.filter(ImageFilter.GaussianBlur(radius=8))
myImage = myImage.filter(ImageFilter.GaussianBlur(radius=4))

# 이미지 저장
myImage.save("rainbow-gradient-pattern.png", bitmap_format="png")

# Tkinter 윈도우에 표시
window = tk.Tk()
window.title("무지개 그라디언트 패턴")
imageTk = ImageTk.PhotoImage(myImage)
tk.Label(window, image=imageTk).pack()
window.mainloop()