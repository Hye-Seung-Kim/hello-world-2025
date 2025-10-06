import React, { useEffect, useRef } from 'react';

const MultiFractalArt = () => {
  const canvasRef = useRef(null);
  
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js';
    script.async = true;
    document.body.appendChild(script);

    script.onload = () => {
      new window.p5((p) => {
        let time = 0;
        
        p.setup = () => {
          p.createCanvas(p.windowWidth, p.windowHeight);
          p.colorMode(p.HSB, 360, 100, 100, 100);
        };
        
        p.windowResized = () => {
          p.resizeCanvas(p.windowWidth, p.windowHeight);
        };
        
        p.draw = () => {
          p.background(0, 0, 5);
          time += 0.01;
          
          p.translate(p.width / 2, p.height / 2);
          
          let scale = Math.min(p.width, p.height) / 1000;
          p.scale(scale);
          
          // Fractal Pattern 1: Recursive Circles
          drawRecursiveCircles(p, 0, 0, 380, 5, time);
          
          // Fractal Pattern 2: Branch fractals
          for (let i = 0; i < 12; i++) {
            p.push();
            p.rotate((360 / 12) * i);
            drawBranchFractal(p, 0, -60, 140, 90, 6, i, time);
            p.pop();
          }
          
          // Fractal Pattern 3: Spiral fractals
          drawSpiralFractal(p, 0, 0, 12, time);
          
          // Fractal Pattern 4: Smaller decorative circles
          drawRecursiveCircles(p, 0, 0, 180, 4, time * 1.5);
        };
        
        function drawRecursiveCircles(p, x, y, size, depth, t) {
          if (depth <= 0 || size < 5) return;
          
          let hue = (depth * 40 + t * 30) % 360;
          let alpha = p.map(depth, 0, 6, 10, 40);
          
          p.noFill();
          p.stroke(hue, 70, 90, alpha);
          p.strokeWeight(2);
          p.circle(x, y, size);
          
          let numCircles = 6;
          let newSize = size / 3;
          let offset = size / 3;
          
          for (let i = 0; i < numCircles; i++) {
            let angle = (p.TWO_PI / numCircles) * i + t * 0.5;
            let nx = x + p.cos(angle) * offset;
            let ny = y + p.sin(angle) * offset;
            
            drawRecursiveCircles(p, nx, ny, newSize, depth - 1, t);
          }
        }
        
        function drawBranchFractal(p, x, y, len, angle, depth, offset, t) {
          if (depth <= 0) return;
          
          let wave = p.sin(t * 2 + offset * 0.5) * 5;
          let hue = (depth * 30 + offset * 30 + t * 50 + 200) % 360;
          let alpha = p.map(depth, 0, 5, 20, 70);
          
          p.stroke(hue, 75, 90, alpha);
          p.strokeWeight(depth * 0.8);
          
          let endX = x + p.cos(p.radians(angle + wave)) * len;
          let endY = y + p.sin(p.radians(angle + wave)) * len;
          
          p.line(x, y, endX, endY);
          
          for (let i = 0; i < 3; i++) {
            let tx = p.lerp(x, endX, i / 3);
            let ty = p.lerp(y, endY, i / 3);
            let size = 3 + p.sin(t * 3 + i) * 1.5;
            
            p.noStroke();
            p.fill(hue, 80, 100, 60);
            p.circle(tx, ty, size);
          }
          
          let newLen = len * 0.67;
          let angleOffset = 25 + p.sin(t) * 10;
          
          drawBranchFractal(p, endX, endY, newLen, angle - angleOffset, depth - 1, offset, t);
          drawBranchFractal(p, endX, endY, newLen, angle + angleOffset, depth - 1, offset, t);
        }
        
        function drawSpiralFractal(p, cx, cy, arms, t) {
          let maxDepth = 100;
          
          for (let arm = 0; arm < arms; arm++) {
            p.beginShape();
            p.noFill();
            
            for (let i = 0; i < maxDepth; i++) {
              let angle = i * 0.3 + (arm * p.TWO_PI / arms) + t * 2;
              let radius = i * 2.5;
              
              let x = cx + p.cos(angle) * radius;
              let y = cy + p.sin(angle) * radius;
              
              let hue = (i * 3 + arm * 45 + t * 60) % 360;
              let alpha = p.map(i, 0, maxDepth, 50, 5);
              
              p.stroke(hue, 85, 95, alpha);
              p.strokeWeight(p.map(i, 0, maxDepth, 3, 0.5));
              p.vertex(x, y);
              
              if (i % 10 === 0) {
                p.push();
                p.noStroke();
                p.fill(hue, 90, 100, alpha * 1.5);
                p.circle(x, y, 4);
                p.pop();
              }
            }
            
            p.endShape();
          }
        }
        
      }, canvasRef.current);
    };

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  return (
    <div className="w-screen h-screen overflow-hidden bg-gray-900">
      <div ref={canvasRef}></div>
    </div>
  );
};

export default MultiFractalArt;