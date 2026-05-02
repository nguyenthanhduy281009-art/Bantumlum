import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. Cấu hình trang
st.set_page_config(page_title="Ultimate Spray - Duy", layout="wide")

# 2. Khởi tạo bộ nhớ Session State cho ảnh nền
if 'bg_base64' not in st.session_state:
    st.session_state.bg_base64 = ""

# --- SIDEBAR ---
st.sidebar.title("🔫 Pro Spray Studio")

# Duy chỉ cần tải ảnh người thôi
bg_file = st.sidebar.file_uploader("👤 Tải ảnh người cần xịt", type=["jpg", "jpeg", "png"])
if bg_file:
    st.session_state.bg_base64 = base64.b64encode(bg_file.read()).decode()

# Thanh chỉnh thông số
p_speed = st.sidebar.slider("🐢 Tốc độ bắn (Chậm)", 5, 15, 8)
p_size = st.sidebar.slider("💧 Cỡ giọt", 1, 6, 2)

if st.sidebar.button("🧹 RESET MÀN HÌNH"):
    st.rerun()

# --- DỮ LIỆU ẢNH ---
img_data = f"data:image/png;base64,{st.session_state.bg_base64}" if st.session_state.bg_base64 else ""

# Đây là mã Base64 của vòi xịt Duy gửi (đã được nhúng sẵn)
# Mình dùng một icon mẫu, Duy có thể thay thế chuỗi này bằng mã Base64 của ảnh Duy nếu muốn vĩnh viễn là ảnh đó
tool_fixed = "https://cdn-icons-png.flaticon.com/512/11496/11496732.png" 

# --- HTML/JS ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {{ margin: 0; padding: 0; overflow: hidden; height: 100%; background: #000; }}
        #bg {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('{img_data}');
            background-size: contain; background-repeat: no-repeat; background-position: center;
            z-index: 1;
        }}
        canvas {{ position: absolute; top: 0; left: 0; z-index: 2; cursor: crosshair; }}
        
        #source-tool {{
            position: fixed; bottom: -5px; left: 50%; transform: translateX(-50%);
            width: 70px; z-index: 3; pointer-events: none;
        }}
    </style>
</head>
<body>
    <div id="bg"></div>
    <img id="source-tool" src="{tool_fixed}">
    <canvas id="sprayCanvas"></canvas>

    <script>
        const canvas = document.getElementById('sprayCanvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        let mouse = {{ x: 0, y: 0, down: false }};
        let frameCounter = 0;

        function resize() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }}

        class Particle {{
            constructor(targetX, targetY) {{
                this.x = canvas.width / 2;
                this.y = canvas.height - 40;
                
                const dx = targetX - this.x;
                const dy = targetY - this.y;
                const dist = Math.sqrt(dx*dx + dy*dy);
                
                const force = {p_speed}; 
                this.vx = (dx / dist) * force + (Math.random() - 0.5) * 1.5;
                this.vy = (dy / dist) * force + (Math.random() - 0.5) * 1.5;
                
                this.size = Math.random() * {p_size} + 0.5;
                this.gravity = 0.08; 
                this.alpha = 1;
                this.decay = 0.005; 
            }}

            update() {{
                this.vy += this.gravity;
                this.x += this.vx;
                this.y += this.vy;
                this.alpha -= this.decay;
            }}

            draw() {{
                ctx.fillStyle = `rgba(255, 255, 240, ${{this.alpha}})`;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }}
        }}

        function handleInput(e) {{
            const x = e.clientX || (e.touches && e.touches[0].clientX);
            const y = e.clientY || (e.touches && e.touches[0].clientY);
            mouse.x = x;
            mouse.y = y;
        }}

        window.addEventListener('mousedown', (e) => {{ mouse.down = true; handleInput(e); }});
        window.addEventListener('mouseup', () => mouse.down = false);
        window.addEventListener('mousemove', handleInput);
        window.addEventListener('touchstart', (e) => {{ mouse.down = true; handleInput(e); }}, {{passive: false}});
        window.addEventListener('touchend', () => mouse.down = false);
        window.addEventListener('touchmove', (e) => {{ handleInput(e); e.preventDefault(); }}, {{passive: false}});

        function animate() {{
            ctx.fillStyle = 'rgba(0, 0, 0, 0.02)';
            
            if(mouse.down) {{
                frameCounter++;
                // Bắn rất chậm: 5 khung hình mới ra 1 hạt
                if (frameCounter % 5 === 0) {{
                    particles.push(new Particle(mouse.x, mouse.y));
                }}
            }}

            for(let i = 0; i < particles.length; i++) {{
                particles[i].update();
                particles[i].draw();
                if(particles[i].alpha <= 0) {{
                    particles.splice(i, 1);
                    i--;
                }}
            }}
            requestAnimationFrame(animate);
        }}

        window.addEventListener('resize', resize);
        resize();
        animate();
    </script>
</body>
</html>
"""

components.html(html_code, height=750)
